<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require 'vendor/autoload.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $title = $_POST['title'];
    $link = $_POST['link'];
    $poster = $_POST['poster'];
    $watchLink = $_POST['watchLink'];
    $releaseDate = $_POST['releaseDate'];
    $format = $_POST['format'];

    // Set up PHPMailer
    $mail = new PHPMailer(true);

    try {
        // Set Gmail SMTP server details
        $mail->isSMTP();
        $mail->Host = 'smtp.gmail.com'; // Use Gmail's SMTP server
        $mail->SMTPAuth = true;
        $mail->Username = 'titumvposting@gmail.com'; // Your Gmail address
        $mail->Password = 'zbbkdssscyjmszfy'; // Your Gmail app password (generate this in your Google account)
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS; // Encryption method
        $mail->Port = 587; // Port for TLS

        // Sender and recipient details
        $mail->setFrom('titumvposting@gmail.com', 'TMDb Movie Fetcher');
        $mail->addAddress('asatkarsarvesh39.titu@blogger.com', 'Blogger'); // Blogger recipient

        // Email subject and body content
        $mail->isHTML(true);
        $mail->Subject = "New Movie: $title";
        $mail->Body = "
            <h3>$title</h3>
            <p><strong>Link:</strong> <a href='$link'>$link</a></p>
            <p><strong>Watch Link:</strong> <a href='$watchLink'>$watchLink</a></p>
            <p><strong>Release Date:</strong> $releaseDate</p>
            <p><strong>Format:</strong> $format</p>
            <img src='$poster' width='200'>
        ";

        // Send the email
        $mail->send();
        echo 'Email sent successfully';
    } catch (Exception $e) {
        echo "Email could not be sent. Mailer Error: {$mail->ErrorInfo}";
    }
}
?>
