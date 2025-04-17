@app.route('/executive/dashboard')
def executive_dashboard():
    if 'user_id' not in session or session['role'] != 'executive':
        return redirect(url_for('login'))
    
    # Summary statistics
    stats = {
        'managers': Manager.query.count(),
        'active_managers': Manager.query.filter_by(is_active=True).count(),
        'agents': Agent.query.count(),
        'active_agents': Agent.query.filter_by(is_active=True).count(),
        'available_stock': Stock.query.filter_by(status='available').count(),
        'today_sales': Sale.query.filter(
            db.func.date(Sale.sale_date) == datetime.today().date()
        ).count(),
        'monthly_sales': Sale.query.filter(
            db.func.strftime('%Y-%m', Sale.sale_date) == datetime.today().strftime('%Y-%m')
        ).count()
    }
    
    # Recent activity
    recent_sales = Sale.query.order_by(Sale.sale_date.desc()).limit(10).all()
    recent_managers = Manager.query.order_by(Manager.created_at.desc()).limit(5).all()
    
    # Performance by manager group
    performance = db.session.query(
        Manager.group_name,
        db.func.count(Sale.id),
        db.func.sum(PhoneModel.price)
    ).join(Sale, Sale.manager_id == Manager.id)\
     .join(Stock, Sale.stock_id == Stock.id)\
     .join(PhoneModel, Stock.model_id == PhoneModel.id)\
     .group_by(Manager.group_name)\
     .all()
    
    return render_template('executive_dashboard.html',
                         stats=stats,
                         recent_sales=recent_sales,
                         recent_managers=recent_managers,
                         performance=performance)