from assassins import *


@app.route('/')
def index():
    recent_kills = Hit.query.filter(Hit.done == True).order_by('done_date desc').limit(5).all()
    leaderboard_members = User.query.order_by('kills desc').limit(10).all()
    return render_template('index.html', recent_kills=recent_kills, leaderboard_members=leaderboard_members)


## media center ##
## password protected ##
@app.route('/media/')
def media():
    pass

## registration, first point of entry ##
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        all_filled = True
        for i in request.form:
            if i == None:
                all_filled = False

        if all_filled:
            username = request.form['username']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            password = sha256_crypt.encrypt(request.form['password'])

            new_user = User(username, first_name, last_name, password, False, 0)
            db.session.add(new_user)
            db.session.flush()
            db.session.commit()
            session['username'] = username
            session['logged_in'] = True
            user = User.query.filter(User.username == username).first()
            return redirect(url_for('dashboard', user=user))
        else:
            flash('You must fill out all fields. Try again')
            return redirect(request.url)

    return render_template('register.html')

## login, second point of entry ##
@app.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        all_filled = True
        for i in request.form:
            if i == None:
                all_filled = False

        if all_filled:
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter(User.username == username).first()

            if sha256_crypt.verify(password, user.password):
                session['logged_in'] = True
                session['username'] = user.username
                flash('Welcome back')
                return redirect(url_for('dashboard', user=user))
            else:
                flash('Incorrect password')
                return redirect(url_for('login'))
        else:
            flash('You must fill out all fields')
            return redirect(url_for('login'))


    return render_template('login.html')


## dashboard ##
@app.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    username = session['username']
    user = User.query.filter(User.username == username).first()
    hit = Hit.query.filter(Hit.a_id == user.id, Hit.done == False).first()
    if hit:
        target = User.query.get(hit.prey_id)
        return render_template('dashboard.html', user=user, hit=hit, target=target)
    else:
        return render_template('dashboard.html', user=user)

## logout ##
@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))

## begin the games. this function is mine. used it to assign the targets ##
@app.route('/begin_the_games/')
@login_required
def begin_games():
    all_users = User.query.all()
    x = []
    for user in all_users:
        x.append(user.id)

    i = 0
    while i < len(x):
        first_user = User.query.get(x[i])
        second_user = User.query.get(x[i-1])
        new_hit = Hit(x[i], x[i-1], first_user.username, second_user.username, False, False, False, None)
        db.session.add(new_hit)
        db.session.flush()
        db.session.commit()
        i+=1
    flash('Let the games begin, Mr. Reid')
    return redirect(url_for('dashboard'))

## dealing with ending the hit ##
@app.route('/been_had/<id>')
def been_had(id):
    relevant_hit = Hit.query.filter(Hit.prey_id == id).first()
    relevant_hit.prey_ver = True
    you = User.query.get(id)
    assassin = User.query.filter(User.id == relevant_hit.a_id).first()

    if relevant_hit.a_ver == True:
        relevant_hit.done = True
        hits_involved_in = Hit.query.filter(Hit.a_id == id).first()
        hits_involved_in.a_id = relevant_hit.a_id
        you.is_out = True
        assassin.kills+=1
        relevant_hit.done_date = datetime.now()
    db.session.commit()
    db.session.flush()
    flash('You\'re out. Thanks for playing. Support your friends!')
    return redirect(url_for('dashboard'))
## yerboi ##
@app.route('/got_them/<id>')
def got_them(id):
    relevant_hit = Hit.query.filter(Hit.prey_id == id).first()
    relevant_hit.a_ver = True
    you = User.query.get(id)
    assassin = User.query.filter(User.id == relevant_hit.a_id).first()
    if relevant_hit.prey_ver == True:
        relevant_hit.done = True
        hits_involved_in = Hit.query.filter(Hit.a_id == id).first()
        hits_involved_in.a_id = relevant_hit.a_id
        you.is_out = True
        assassin.kills+=1
        relevant_hit.done_date = datetime.now()
    db.session.commit()
    db.session.flush()
    flash('You\'ve made it this far. Keep going')
    return redirect(url_for('dashboard'))
