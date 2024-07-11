<?php
$host = "127.0.0.1";
$port = "5432";
$dbname = "tenant";
$user = "postgres";
$password = "password";

$conn = pg_connect("host=$host port=$port dbname=$dbname user=$user password=$password");

if (!$conn) {
    die("Connection failed: " . pg_last_error());
}

$sql = "SELECT id, name, age, date_of_birth, contact_number, plan_subscription, status FROM todo_api_tenant";
$result = pg_query($conn, $sql);

if (!$result) {
    die("Query failed: " . pg_last_error());
}
?>

<!DOCTYPE HTML>
<html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            @page {
                size: A4;
                margin: 20mm;
            }

            .content {
                width: 210mm; 
                height: 297mm;
                margin: auto;
            }

            table {
                width: 80%;
                table-layout: auto; 
                border-collapse: collapse;
                margin: 0 auto;
            }
            th, td {
                padding: 8px;
                text-align: center; 
            }
            footer {
                bottom: 0;
                width: 80%;
                text-align: center;
                margin: 0 auto;
            }

            hr {
                display: block;
                height: 2px;
                background: transparent;
                width: 80%;
                border: none;
                border-top: solid 2px #000000;
            }

        </style>
        <script>
            function displayDateTime() {
                const now = new Date();
                const dateTimeString = now.toLocaleString();
                document.getElementById('date-time').innerText = dateTimeString;
            }
    
            window.onload = displayDateTime;
        </script>
    
    </head>
    <body class="content">
    <header>
        <h1 style="text-align: center;">TENANT REPORT</h1>
        <hr>
    </header>

    <table>
        <thead style="background-color:lightgray">
            <tr>
                <th>ID</th>
                <th>NAME</th>
                <th>AGE</th>
                <th>BIRTH DATE</th>
                <th>CONTACT</th>
                <th>PLAN</th>
                <th>STATUS</th>
            </tr>
        </thead>
        <tbody>
            <?php
            while ($row = pg_fetch_assoc($result)) {
                echo 
                "<tr>
                    <td>" . htmlspecialchars($row["id"]) . "</td>
                    <td>" . htmlspecialchars($row["name"]) . "</td>
                    <td>" . htmlspecialchars($row["age"]) . "</td>
                    <td>" . htmlspecialchars($row["date_of_birth"]) . "</td>
                    <td>" . htmlspecialchars($row["contact_number"]) . "</td>
                    <td>" . htmlspecialchars($row["plan_subscription"]) . "</td>
                    <td>" . htmlspecialchars($row["status"]) . "</td>
                </tr>";
            }
            pg_free_result($result);
            pg_close($conn);
            ?>
        </tbody>
    </table>
    <br>

    <hr>

    <footer class="footer">
        Generated on: <span id="date-time"></span>
    </footer>
</body>
</html>