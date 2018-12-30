<h2>Project_par</h2>


  <p>This project is based on the <b>theory of Markowitz</b>, it gives you the possibility to simulate the portfolio and to know in wich companies you have to invest depending on you preference. The application uses the data of Google Finance.</p>
  
  <p>
  The two graphs that are being returned by the website are respectivly Efficient frontier with no risk-free asset and the ratios to invest in each company based on you preference, if you want to minimize the risk wich is equivalent to minimizing the variance, you have to choose the ratios with the blue color otherwise, if you want to maximize the profit and accepting more risk, you have to choose the ratios with the red color.
  </p>
  
  <p>
  To install the web page locally, you must install python and make sure that pip is registered as a local variable. When you finish the installation, go to the command prompt and write "pip install <b>name of the library</b>". The libararies are 
  </p>

<ul>
  <li>dj-database-url</li>
  <li>Django</li>
  <li>gunicorn</li>
  <li>matplotlib</li>
  <li>numpy</li>
  <li>panda</li>
<li>pandas</li>
  <li>psycopg2</li>
  <li>pandas-datareader</li>
  <li>pbr</li>
<li>plotly</li>
  <li>scipy</li>
  <li>whitenoise</li>
  <li>pillow</li>
</ul>

<p>
 Now that you finished this first step, clone the repository by using git Bash, write on it "git clone <b>the name of the repository</b>". 
</p>

<p>
  With command prompt go to the folder and open it, write the command "python manage.py makemigrations" if you are using Linux, with windows write "python manage.py makemigrations", do the same thing this time with migrate unstead of makemigrations. Now create a user by typing on the command prompt "python manage.py createsuperuser", it will ask you to enter a username, a mail adresse, and a password and to confirme the password, after this step you can run the server locally, type "python manage.py runserver", the web page is running locally.
</p>

<ul>
  <li>Go to the admin page by typing in your browser "localhost:8000/admin", The admin page show something like that <img src="https://github.com/sarrme/project_par/blob/master/admin%20page.PNG"></img></li>
  <br/>
  <li>Double clique on <b>choix actifs</b> in the admin page. You have to specify companies, you can not specify what ever you want, it is not possible because it required changing things in the code, if want want to know how to do it, feel free to contact me by clicking <a href="mailto:sarroukh.issame@gmail.com?&subject=Questions&body=Mettre%20your%20questions%20here">this link</a></li>
</ul>

