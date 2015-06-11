It was a simple blog demo.

I don't write register part.

If you want create user, you should use 
    
    python manager shell
    db.create_all()
    u = User(email='',username='',password='')
    db.session.add(u)
    db.session.commit

or you create it in MySQL.