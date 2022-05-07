<h1 style="text-align:center;font-family:Gill Sans, sans-serif">CS5394 Project3</h1>
<img src="images/logo.png"
     alt="Markdown Monster icon"
     style="float: center; margin-right: 10px;" />
<h2 style="color:dodgerblue;">Mario Kart Wii Mogi Lounge MMR predictor </h1>
<h4>Background Info</h4>

<p style="font-family:courier;">Mario Kart Wii is one of my favorite games and has been for over 10 years.</p>
<p style="font-family:courier;">With the evolulion of the game a competetive comunity has formed and there are thousands of players playing daily.</p>
<p style="font-family:courier;">There are 32 track in the game nativly and you can see your statistics on all the tracks through the matches you have played</p>
<p style="font-family:courier;">My goal was to make and train a model to predict a players mmr based on their<ul style=" font-family:courier;"><li>Average Placement</li><li>Fastest Time</li><li>Number of Times played</li></ul></p>



<p>These elements were chosen because they are quickly accesible for all players using the command <br><code style="font-size330%;">?besttracks rt</code> in the main community discord server.</p>

<h4>Data Retrieval</h4>
<p style="font-family:courier;">The data for all the races is held in a private  data base, and while I am in contact with the administrators to potentially have access to this data in the future I was not able to for this project.</p>
<p style="font-family:courier;">To circumvent this I used the lounge website as my datasource and used bs4 to web scrape from each indiviuduals page.</p>
<p style="font-family:courier;">Here is my page that I webscraped
<img src="images/data.png"
     alt="Markdown Monster icon"
     style="float: center; margin-right: 10px;" />this conatins my data and is updated every hour.</p>





