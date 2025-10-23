from datetime import datetime
import os
from fpdf import FPDF

def generate_contract(advance, user, advance_details):
    """
    Generate a digital contract for the cash advance.
    
    Args:
        advance: The Advance object
        user: The User object
        advance_details: Dictionary containing advance details
        
    Returns:
        str: Path to the generated contract PDF
    """
    # Create contracts directory if it doesn't exist
    contracts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'contracts')
    os.makedirs(contracts_dir, exist_ok=True)
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Add header
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'LoanlessPay Cash Advance Agreement', 0, 1, 'C')
    pdf.ln(10)
    
    # Add contract details
    pdf.set_font('Arial', '', 12)
    
    # Contract ID and Date
    pdf.cell(0, 10, f'Contract ID: {advance.contract_id}', 0, 1)
    pdf.cell(0, 10, f'Date: {datetime.now().strftime("%Y-%m-%d")}', 0, 1)
    pdf.ln(5)
    
    # User Information
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'User Information', 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Name: {user.first_name} {user.last_name}', 0, 1)
    pdf.cell(0, 10, f'Email: {user.email}', 0, 1)
    pdf.cell(0, 10, f'Phone: {user.phone_number}', 0, 1)
    pdf.ln(5)
    
    # Advance Details
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Advance Details', 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Advance Amount: ${advance.amount:.2f}', 0, 1)
    pdf.cell(0, 10, f'Commission (2%): ${advance_details["commission"]:.2f}', 0, 1)
    pdf.cell(0, 10, f'Total Repayment: ${advance_details["total_repayment"]:.2f}', 0, 1)
    pdf.cell(0, 10, f'Number of Installments: {advance.installments}', 0, 1)
    pdf.cell(0, 10, f'Monthly Installment: ${advance_details["installment_amount"]:.2f}', 0, 1)
    pdf.ln(5)
    
    # Payment Schedule
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Payment Schedule', 0, 1)
    pdf.set_font('Arial', '', 12)
    
    for i, payment_date in enumerate(advance_details['payment_dates']):
        payment_amount = advance_details['installment_amounts'][i] if 'installment_amounts' in advance_details else advance_details['installment_amount']
        pdf.cell(0, 10, f'Payment {i+1}: ${payment_amount:.2f} due on {payment_date.strftime("%Y-%m-%d")}', 0, 1)
    
    pdf.ln(10)
    
    # Terms and Conditions
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Terms and Conditions', 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, '1. This is an interest-free cash advance.\n2. A fixed 2% commission is applied to the advance amount.\n3. Payments are due on the dates specified in the payment schedule.\n4. Late payments may affect your eligibility for future advances.\n5. By accepting this advance, you agree to repay the full amount according to the schedule.')
    
    pdf.ln(10)
    
    # Signature
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Signatures', 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'User Signature: _______________________', 0, 1)
    pdf.cell(0, 10, 'Date: _______________________', 0, 1)
    pdf.ln(5)
    pdf.cell(0, 10, 'LoanlessPay Representative: _______________________', 0, 1)
    pdf.cell(0, 10, 'Date: _______________________', 0, 1)
    
    # Save PDF
    contract_filename = f'contract_{advance.contract_id}.pdf'
    contract_path = os.path.join(contracts_dir, contract_filename)
    pdf.output(contract_path)
    
    return contract_path