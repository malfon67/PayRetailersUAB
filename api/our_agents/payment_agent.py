import requests
from agents import Agent, function_tool
from our_agents_definition.base_agent import BaseAgentOutput, BASE_STARTING_PROMPT
from typing import Optional

class PaymentAgentOutput(BaseAgentOutput):
    """
    Output model for the Payment Agent.
    """
    transaction_id: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None

@function_tool
def initiate_payment(amount: float, currency: str, recipient: str) -> dict:
    """
    Initiate a payment using PayRetailers API.
    
    Parameters:
    - amount: Payment amount
    - currency: Currency code (e.g., USD, EUR)
    - recipient: Recipient identifier (email or name)
    
    Returns:
    - Payment initiation result in JSON format
    """
    print(f"Payment Agent is initiating a payment. Amount: {amount}, Currency: {currency}, Recipient: {recipient}")
    try:
        # Updated to use sandbox credentials and endpoint
        url = "https://api-sandbox.payretailers.com/payments/v2/transactions"
        payload = {
            "paymentMethodId": "b04f2ffd-0751-4771-9d07-e9c866977896",  # Example payment method ID
            "amount": str(amount),
            "currency": currency,
            "description": "Payment initiated via Payment Agent",
            "trackingId": "Test-Tracking",
            "notificationUrl": "https://beeceptor.com/notification",
            "returnUrl": "https://beeceptor.com/return",
            "cancelUrl": "https://beeceptor.com/cancel",
            "language": "ES",
            "customer": {
                "firstName": "Prueba",
                "lastName": "Test",
                "email": recipient,
                "country": "BR",
                "personalId": "49586181049",
                "city": "Buenos Aires",
                "address": "dsa",
                "zip": "130",
                "phone": "1149682315",
                "deviceId": "DEVICE",
                "ip": "181.166.176.12"
            }
        }
        headers = {
            "Authorization": "Basic MTAwMDE1ODY6MDlhNWFmZDE2NzkwMzRmMjcwNjFlZTRhMTlhMjFkM2FjYzk0Yzg3M2IzNzJjN2E0YTg1YjY0MTE1ZjQwNGIwOA=="
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return {"agent_type": "payment", "status": "success", "transaction_id": data.get("transaction_id"), "message": "Payment successful"}
        else:
            return {"agent_type": "payment", "status": "error", "message": f"Error initiating payment: {response.status_code}, {response.text}"}
    except Exception as e:
        return {"agent_type": "payment", "status": "error", "message": f"Error during payment initiation: {str(e)}"}

@function_tool
def check_payment_status(transaction_id: str) -> dict:
    """
    Check the status of a payment using PayRetailers API.
    
    Parameters:
    - transaction_id: The transaction ID to check
    
    Returns:
    - Payment status in JSON format
    """
    print(f"Payment Agent is checking payment status. Transaction ID: {transaction_id}")
    try:
        # Placeholder for PayRetailers API endpoint
        url = f"https://api.payretailers.com/v1/payments/{transaction_id}"
        headers = {"Authorization": "Bearer YOUR_API_KEY"}  # Replace with actual API key
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return {"agent_type": "payment", "status": "success", "data": data}
        else:
            return {"agent_type": "payment", "status": "error", "message": f"Error checking payment status: {response.status_code}"}
    except Exception as e:
        return {"agent_type": "payment", "status": "error", "message": f"Error during status check: {str(e)}"}

payment_agent = Agent(
    name="Payment Agent",
    instructions=(
        BASE_STARTING_PROMPT +
        "Ayuda a los usuarios a realizar pagos utilizando PayRetailers. Genera tu salida en formato JSON, y esta será transformada a HTML por el HTMLTransformer. "
        "Responde solo en español."
    ),
    tools=[initiate_payment, check_payment_status],
    handoff_description="Assists with payment processing using PayRetailers.",
    output_type=PaymentAgentOutput
)

# Expose the agent instance for dynamic imports
agent_instance = payment_agent
