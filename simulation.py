from datetime import datetime, timedelta

def calculate_advance_details(amount, installments):
    """
    Calculate advance details including commission, total repayment, installment amount,
    and payment dates.
    
    Args:
        amount (float): The advance amount requested
        installments (int): Number of installments for repayment
        
    Returns:
        dict: Dictionary containing advance details
    """
    # Calculate commission (2% of advance amount)
    commission = amount * 0.02
    
    # Calculate total repayment (advance amount + commission)
    total_repayment = amount + commission
    
    # Calculate installment amount
    installment_amount = round(total_repayment / installments, 2)
    
    # Calculate payment dates (monthly)
    payment_dates = []
    for i in range(1, installments + 1):
        payment_date = datetime.now() + timedelta(days=30 * i)
        payment_dates.append(payment_date)
    
    # Ensure the total matches by adjusting the last payment if needed
    total_installments = installment_amount * installments
    if abs(total_installments - total_repayment) > 0.01:
        # Adjust the last payment to account for rounding differences
        last_payment = installment_amount + (total_repayment - total_installments)
        installment_amounts = [installment_amount] * (installments - 1) + [round(last_payment, 2)]
    else:
        installment_amounts = [installment_amount] * installments
    
    return {
        'advance_amount': amount,
        'commission': commission,
        'total_repayment': total_repayment,
        'installment_amount': installment_amount,
        'installment_amounts': installment_amounts,
        'payment_dates': payment_dates,
        'installments': installments
    }

def get_payment_schedule(advance_details):
    """
    Generate a payment schedule based on advance details.
    
    Args:
        advance_details (dict): Dictionary containing advance details
        
    Returns:
        list: List of dictionaries containing payment schedule
    """
    schedule = []
    
    for i in range(len(advance_details['payment_dates'])):
        payment = {
            'payment_number': i + 1,
            'due_date': advance_details['payment_dates'][i].strftime('%Y-%m-%d'),
            'amount': advance_details['installment_amounts'][i]
        }
        schedule.append(payment)
    
    return schedule