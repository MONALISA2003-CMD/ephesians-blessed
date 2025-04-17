@app.route('/executive/managers')
def executive_managers():
    if 'user_id' not in session or session['role'] != 'executive':
        return redirect(url_for('login'))
    
    managers = Manager.query.order_by(Manager.group_name).all()
    return render_template('executive_managers.html', managers=managers)

@app.route('/executive/add-manager', methods=['GET', 'POST'])
def add_manager():
    if 'user_id' not in session or session['role'] != 'executive':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Process form data
        manager_data = {
            'full_name': request.form['full_name'],
            'region': request.form['region'],
            'districts': request.form['districts'],
            'phone': request.form['phone'],
            'email': request.form['email'],
            'group_name': request.form['group_name'],
            'executive_id': session['user_id']
        }
        
        # Handle file uploads
        if 'id_front' in request.files and 'id_back' in request.files:
            front = request.files['id_front']
            back = request.files['id_back']
            profile = request.files['profile_photo']
            
            # Save files (implementation depends on your storage system)
            front_path = save_uploaded_file(front, 'manager_ids')
            back_path = save_uploaded_file(back, 'manager_ids')
            profile_path = save_uploaded_file(profile, 'manager_photos')
            
            manager_data['id_photos'] = json.dumps({
                'front': front_path,
                'back': back_path
            })
            manager_data['profile_photo'] = profile_path
        
        # Create manager
        new_manager = Manager(**manager_data)
        db.session.add(new_manager)
        
        # Create login credentials
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        user = User(
            username=username,
            password=password,
            role='manager',
            manager_id=new_manager.id
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Manager added successfully!', 'success')
        return redirect(url_for('executive_managers'))
    
    return render_template('add_manager.html')

def save_uploaded_file(file, subfolder):
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return filepath
    return None