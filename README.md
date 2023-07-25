склонить проект и переименновать  <strong>env.save на .env </strong>

Первая комманда, ну и последняя <br />
docker-compose up --build

http://127.0.0.1:8080/upload - <br />
POST request form-data body: <br />
<h4> key: image value: file </h4>
<h4> key: width value: int default: 300 </h4>
<h4> key: height value: int default: 300 </h4>
<h3> Response token: uuid </h3>
этот токет вставляете в запрос

http://127.0.0.1:8080/upload/<token> - <br />
GET request <br />
в ответ получаете ответ с ссылкой на обрезанный image