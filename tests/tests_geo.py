def test_app(apps):
    assert apps.name == 'main'    

def test_collections(db):
    assert 'users' in db.list_collection_names()
    assert 'pontos' in db.list_collection_names()

def test_users(db):
    usuario = db.users.find_one({'email': 'p@p'})
    print(usuario['nome'])
    assert usuario['nome'] == 'marcus'

def test_post_usuario(client):
    response = client.post("http://localhost:8080/AdicionarUsuario/?email=test@gmail.com&nome=test")
    assert response.status_code == 201
    
def test_post_ponto(client):
    response = client.post("http://localhost:8080/AdicionarPonto/?latitude=-45.8952&longitude=38.5648&email=test@gmail.com")
    assert response.status_code == 201

def test_get_usuario(client):
    response = client.get("http://localhost:8080/VerUsuarios")
    assert response.status_code == 200

def test_del_usuario(client):
    response = client.delete("http://localhost:8080/RemoverUsuario/?email=test@gmail.com")
    assert response.status_code == 200

def test_del_ponto(client):
    response = client.delete("http://localhost:8080/RemoverPonto/?id=62f7f4de8e1d8e77bc3209c5&user=test")
    assert response.status_code == 200


