<?php

// Define some constants
define( "RECIPIENT_NAME", "Scuba" );
define( "RECIPIENT_EMAIL", "info@scubadivingadventure.in" );


// Read the form values
$success = false;
$senderName = isset( $_POST['username'] ) ? preg_replace( "/[^\s\S\.\-\_\@a-zA-Z0-9]/", "", $_POST['username']) : "";
$senderPhone = isset( $_POST['phone'] ) ? preg_replace( "/[^\.\-\_\@a-zA-Z0-9]/", "", $_POST['phone'] ) : "";
$senderEmail = isset( $_POST['email'] ) ? preg_replace( "/[^\.\-\_\@a-zA-Z0-9]/", "", $_POST['email'] ) : "";
$senderTripdate = isset( $_POST['tripdate'] ) ? preg_replace( "/[^\.\-\_\@a-zA-Z0-9]/", "", $_POST['tripdate'] ) : "";
$senderGuest = isset( $_POST['guest'] ) ? preg_replace( "/[^\.\-\_\@a-zA-Z0-9]/", "", $_POST['guest'] ) : "";
$senderService1 = isset( $_POST['check-1'] ) ? preg_replace( "/[^\.\-\_\@a-zA-Z0-9]/", "", $_POST['check-1'] ) : "";
$senderService2 = isset( $_POST['check-2'] ) ? preg_replace( "/[^\.\-\_\@a-zA-Z0-9]/", "", $_POST['check-2'] ) : "";
$senderService3 = isset( $_POST['check-3'] ) ? preg_replace( "/[^\.\-\_\@a-zA-Z0-9]/", "", $_POST['check-3'] ) : "";
$senderService4 = isset( $_POST['check-4'] ) ? preg_replace( "/[^\.\-\_\@a-zA-Z0-9]/", "", $_POST['check-4'] ) : "";


// If all values exist, send the email
if ( $senderName && $senderPhone) {
  $recipient = RECIPIENT_NAME . " <" . RECIPIENT_EMAIL . ">";
  $headers = "From: " . $senderName . "";
  $msgBody = "Name: ". $senderName . " Email: ". $senderEmail . "Phone: ". $senderPhone . " Tripdate: ". $senderTripdate . " Guest: " . $senderGuest . "Tourpackage: ". $senderService1 . "Scubadiving: ". $senderService2 . "Watersports: ". $senderService3 . "Boattour: ". $senderService4 . "";
  $success = mail( $recipient, $headers, $msgBody );

  //Set Location After Successsfull Submission
  header('Location: contact2.html?message=Successfull');
  echo "Thankyou for response. Your Booking Details has been sent successfully. Our Team will contact you soon.";
}

else{
	//Set Location After Unsuccesssfull Submission
  	header('Location: contact.html?message=Failed');
    echo "Your Response is not recorded. Please Try Again!";	
}

?>