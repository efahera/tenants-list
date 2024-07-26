<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Report Generator</title>
        
        <style>

        .page {
            margin: 50px;
        }
        .container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .homebutton {
            display: inline-block;
            background-color: #e1e1e1;
            color: rgb(0, 0, 0);
            text-align: center;
            text-decoration: none;
            border: 1px solid rgb(0, 0, 0);
            cursor: pointer;
            padding: 2px 5px;
            font-size: 13px;
            margin: 0 auto;
            align-items: center;
            align-content: center;
            left: 50%;
            right: 50%;
        }

        .homebutton:hover {
            background-color:darkgray;
            color: white; }

        </style>
        <script>

        </script>
    </head>

    <body>
        <div class="page">
            
            <div> <!-- HOME TITLE --> <u><h1 style="text-align: center;"> REPORT GENERATOR </h1></u></div>

            <div> <!-- SELECT REPORT --> <h3 style="text-align: center; padding: 20px">Select type of report:</h3></div>
                
            <div class="container"> <!-- BUTTONS -->
                
                <div style ="display: flex; gap: 10px">
                    <div><a href="tenant_report.php" class="homebutton"><b>TENANT</b></a></div>
                    <div><a href="subscriber_report.php" class="homebutton"><b>SUBSCRIBER</b></a></div>
                    <div><a href="subscription_report.php" class="homebutton"><b>SUBSCRIPTION</b></a></div>
                </div>
                
                <br>

                <div style ="display: flex; gap: 10px">
                    <div><a href="tenant_id_report.php" class="homebutton"><b>TENANT BY USER ID</b></a></div>                
                    <div><a href="subscriber_id_report.php" class="homebutton"><b>SUBSCRIBER BY USER ID</b></a></div>                
                </div>
                
                <br>
                
            </div>


            </div>
        </div>
    </body>
        
</html>    