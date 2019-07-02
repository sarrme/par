<h2>Project_par</h2>


  <p>This project is based on <b>Markowitz's theory</b>, it gives you the opportunity to simulate the portfolio and know which companies you should invest in according to your preferences. The app uses data extracted from Google Finance.</p>
  <p>
  
The site collects the data and then processes it. This data is in the form of a data block, which facilitates the elimination of missing data and the calculation of mean and variance. 
  </p>
  <p>
  
The two graphs returned by the website are respectively Effective Frontier without risk-free assets and the ratios to invest in each company according to your preferences, if you want to minimize the risk that equates to minimizing the variance, you have to: choose the ratios with the blue color, otherwise, if you want to maximize profits and accept more risk, you must choose the ratios with the color red.
  <img src="3.PNG"/>
  <img src="4.PNG"/>
  </p>
  
  <p>
  To run the web page locally, you must install Python 3 and make sure pip is registered as a local variable. When you have completed the installation, go to the command prompt and write "pip install <b>name of the library</b>". Libraries are:
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
 
Now that you've completed this first step, clone the repository using the git Bash command prompt, write on it "git clone <b>the name of the repository</b>". 
</p>

<p>
  With command prompt go to the folder and open it, write the command "python manage.py makemigrations" if you are using Linux, with windows write "py manage.py makemigrations", do the same thing this time with migrate instead of makemigrations. Now create a user by typing on the command prompt "py manage.py createsuperuser", it will ask you to enter a username, a mail adress, and a password and to confirm the password, after this step you can run the server locally, type "python manage.py runserver", the web page is running locally.
</p>

<ul>
  <li>Go to the admin page by typing in your browser "localhost:8000/admin", The admin page displays something like this <img src="https://github.com/sarrme/par/blob/master/admin%20page.PNG"></img></li>
  <br/>
  <li>Double click on <b>choix actifs</b> in the admin page. You have to specify companies by clicking on <b>add choix actif</b>, the list of companies that you can choose from is <b>AMAZON, APPLE, EXXON, FORD, GOOGLE, WALMART</b>, the name of the company must be writting in the form field <b>Nom d'entreprise</b> with capital letters, and without spaces, you can not specify what ever you want, it is not possible because you will have to modify the code, if you want to know how to proceed, do not hesitate to contact me by clicking on <a href="mailto:sarroukh.issame@gmail.com?&subject=Questions&body=Put%20your%20questions%20here">this link</a>. Images can be used directly from the folder, you can find them on media / logos. You have to create a simulation by double clicking on <b>simulations</b> and  then clicking on <b>add simulation</b>. You can specify what ever you want for images and dates, this step is necessary for the website to work properly. If you want real pictures that I used, go to simulation/first and simulation/second and add those two pictures.</li>
</ul>

<p>After all these steps, the site works, to specify new variables for your simulation, connect to the site by clicking on "se connecter" then on simulation and click on "changer paramètres", use new variables, after the calculation, you will be redirected to the result of your simulation.</p>
<p> I will leave you with some screenshots of the website</p>
<img src="1.PNG"/>
<img src="2.PNG"/>
<img src="3.PNG"/>
<img src="4.PNG"/>
<img src="6.PNG"/>
<img src="7.PNG"/>
<img src="8.PNG"/>
<img src="9.PNG"/>
<p>That's all, thank you for reading all this, best wishes,</p>
<p><b>SARROUKH Issame</b></p>

