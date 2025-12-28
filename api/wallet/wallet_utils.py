

# O sistema de convite funciona assim: O owner cria a transação, uma verificação é feita: If is_shared, então o sistema ira enviar de alguma forma um popup com um gatilho.
# Esse popup possui algumas infos basicas para um crud da transação em questão, ou seja o id do owner e o id da transação. 
#Quando o usuario clica em abrir o popup um GET é disparado pra buscar as informaçoes da transação: quem, quando, valor total e valor do counterparty e um campo de descrição. 
# O counterparty ao validar ele envia um post na rota basica de criação de transação e essa transação entra como se fosse uma criação propria dele, porem invertendo os papeis

