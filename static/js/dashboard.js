<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>ClaraVerse • Portal</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body class="dashboard-inicial">
    <div class="container-dashboard">
        <img src="{{ url_for('static', filename='logo_claraverse.png') }}" alt="Logo ClaraVerse" class="logo">
        <h1>Bem-vindo ao ClaraVerse</h1>
        <p>Sua central de inteligência automatizada e decisões invisíveis em tempo real.</p>
        
        <div class="botoes-dashboard">
            <a href="{{ url_for('login') }}" class="btn-principal">✨ Entrar</a>
            <a href="{{ url_for('configurar') }}" class="btn-secundario">⚙️ Configurar</a>
        </div>
    </div>
</body>
</html>