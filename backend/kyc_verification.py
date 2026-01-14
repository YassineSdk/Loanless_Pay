from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from models import db, User, KYCDocument
from werkzeug.utils import secure_filename
from datetime import datetime
import os

kyc = Blueprint('kyc', __name__, url_prefix='/kyc')

# File upload configuration
UPLOAD_FOLDER = os.path.join("static", "kyc_documents")
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_size(file):
    """Get file size in bytes"""
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size


# ============================================================================
# USER-FACING ROUTES - KYC Verification
# ============================================================================

@kyc.route('/')
@login_required
def index():
    """KYC verification status page"""
    # Get user's KYC documents
    documents = KYCDocument.query.filter_by(user_id=current_user.id).all()

    return render_template('kyc/index.html',
                          user=current_user,
                          documents=documents)


@kyc.route('/verify')
@login_required
def verify():
    """KYC verification form"""
    # Check if already approved
    if current_user.kyc_status == 'approved':
        flash('Your KYC verification is already approved.', 'info')
        return redirect(url_for('kyc.index'))

    # Get existing documents
    documents = KYCDocument.query.filter_by(user_id=current_user.id).all()

    return render_template('kyc/verify.html',
                          user=current_user,
                          documents=documents)


@kyc.route('/submit', methods=['POST'])
@login_required
def submit():
    """Submit KYC information"""
    # Check if already approved
    if current_user.kyc_status == 'approved':
        return jsonify({'success': False, 'message': 'KYC already approved'}), 400

    # Update user information
    current_user.full_name = request.form.get('full_name')
    current_user.date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d').date() if request.form.get('date_of_birth') else None
    current_user.address = request.form.get('address')
    current_user.nationality = request.form.get('nationality')
    current_user.phone_number = request.form.get('phone_number')
    current_user.national_id_number = request.form.get('national_id_number')
    current_user.gender = request.form.get('gender')

    # Mark as submitted
    current_user.kyc_submitted = True
    current_user.kyc_submitted_at = datetime.utcnow()
    current_user.kyc_status = 'pending'

    db.session.commit()

    flash('KYC information submitted successfully! Please wait for admin approval.', 'success')
    return redirect(url_for('kyc.index'))


@kyc.route('/upload-document', methods=['POST'])
@login_required
def upload_document():
    """Upload KYC document"""
    # Check if already approved
    if current_user.kyc_status == 'approved':
        return jsonify({'success': False, 'message': 'KYC already approved'}), 400

    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400

    file = request.files['file']
    document_type = request.form.get('document_type')

    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'File type not allowed. Use PDF, JPG, or PNG'}), 400

    # Check file size
    file_size = get_file_size(file)
    if file_size > MAX_FILE_SIZE:
        return jsonify({'success': False, 'message': 'File size exceeds 10MB limit'}), 400

    # Save file
    filename = secure_filename(f"{current_user.id}_{document_type}_{datetime.utcnow().timestamp()}_{file.filename}")
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Check if document type already exists, if so delete the old one
    existing_doc = KYCDocument.query.filter_by(
        user_id=current_user.id,
        document_type=document_type
    ).first()

    if existing_doc:
        # Delete old file
        if os.path.exists(existing_doc.file_path):
            os.remove(existing_doc.file_path)
        # Delete old record
        db.session.delete(existing_doc)

    # Create document record
    document = KYCDocument(
        user_id=current_user.id,
        document_type=document_type,
        document_name=file.filename,
        file_path=file_path,
        file_size=file_size,
        mime_type=file.content_type
    )
    db.session.add(document)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Document uploaded successfully',
        'document': document.to_dict()
    })


@kyc.route('/document/<int:document_id>/delete', methods=['POST'])
@login_required
def delete_document(document_id):
    """Delete a KYC document"""
    document = KYCDocument.query.get_or_404(document_id)

    # Verify ownership
    if document.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    # Check if KYC already approved
    if current_user.kyc_status == 'approved':
        return jsonify({'success': False, 'message': 'Cannot delete documents after KYC approval'}), 400

    # Delete file from filesystem
    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    # Delete from database
    db.session.delete(document)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Document deleted successfully'})


@kyc.route('/document/<int:document_id>/download')
@login_required
def download_document(document_id):
    """Download a KYC document"""
    document = KYCDocument.query.get_or_404(document_id)

    # Verify ownership or admin
    if document.user_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access', 'error')
        return redirect(url_for('kyc.index'))

    return send_file(document.file_path, as_attachment=True, download_name=document.document_name)


@kyc.route('/status')
@login_required
def status():
    """Get KYC status (API endpoint)"""
    documents = KYCDocument.query.filter_by(user_id=current_user.id).all()

    return jsonify({
        'success': True,
        'kyc_status': current_user.kyc_status,
        'kyc_submitted': current_user.kyc_submitted,
        'kyc_submitted_at': current_user.kyc_submitted_at.isoformat() if current_user.kyc_submitted_at else None,
        'kyc_approved_at': current_user.kyc_approved_at.isoformat() if current_user.kyc_approved_at else None,
        'documents_count': len(documents),
        'has_national_id': any(doc.document_type == 'national_id' for doc in documents),
        'has_proof_of_address': any(doc.document_type == 'proof_of_address' for doc in documents)
    })
