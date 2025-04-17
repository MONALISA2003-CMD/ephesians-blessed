@app.route('/receipt/<receipt_number>')
def generate_receipt(receipt_number):
    sale = Sale.query.filter_by(receipt_number=receipt_number).first_or_404()
    stock = Stock.query.get(sale.stock_id)
    model = PhoneModel.query.get(stock.model_id)
    agent = Agent.query.get(sale.agent_id)
    manager = Manager.query.get(sale.manager_id)
    
    # Create PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Header
    p.setFont("Helvetica-Bold", 18)
    p.drawString(100, 780, "EPHESIANS BLESSED PHONE ACCESSORIES")
    p.setFont("Helvetica", 12)
    p.drawString(100, 760, "Location: KAMPALA | Tel: +256 703 953711")
    p.line(100, 755, 500, 755)
    
    # Receipt Info
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 730, "OFFICIAL SALES RECEIPT")
    p.setFont("Helvetica", 10)
    p.drawString(100, 710, f"Receipt #: {sale.receipt_number}")
    p.drawString(300, 710, f"Date: {sale.sale_date.strftime('%d/%m/%Y %H:%M')}")
    
    # Item Details
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, 680, "ITEM SOLD:")
    p.setFont("Helvetica", 10)
    p.drawString(120, 660, f"Model: {model.model_name} {model.storage}")
    p.drawString(120, 640, f"IMEI: {stock.imei}")
    p.drawString(120, 620, f"Price: UGX {model.price:,.2f}")
    
    # Agent Info
    p.drawString(350, 660, f"Sold by: {agent.full_name}")
    p.drawString(350, 640, f"Manager: {manager.full_name}")
    p.drawString(350, 620, f"Group: {manager.group_name}")
    
    # Customer Details
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, 580, "CUSTOMER DETAILS:")
    p.setFont("Helvetica", 10)
    p.drawString(120, 560, f"Name: {sale.customer_name}")
    p.drawString(120, 540, f"Phone: {sale.customer_phone}")
    p.drawString(120, 520, f"Next of Kin: {sale.customer_nok}")
    
    # Terms and Conditions
    p.setFont("Helvetica-Bold", 10)
    p.drawString(100, 480, "TERMS & CONDITIONS:")
    p.setFont("Helvetica", 8)
    terms = [
        "1. This receipt serves as proof of purchase",
        "2. Warranty covers manufacturing defects only",
        "3. Devices must be returned in original condition",
        "4. Contact manager for any after-sale issues"
    ]
    for i, term in enumerate(terms):
        p.drawString(120, 460 - (i * 15), term)
    
    # Footer
    p.line(100, 400, 500, 400)
    p.setFont("Helvetica-Bold", 10)
    p.drawString(100, 380, "THANK YOU FOR YOUR BUSINESS!")
    p.drawString(100, 360, "www.ephesiansblessed.com | Email: kabuusumonalisa@gmail.com")
    
    p.showPage()
    p.save()
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True,
                   download_name=f"EPHESIANS_RECEIPT_{receipt_number}.pdf",
                   mimetype='application/pdf')