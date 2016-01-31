<?php
require_once 'firebaseLib.php';
// --- This is your Firebase URL
$url = 'https://washtime.firebaseio.com/';
// --- Use your token from Firebase here
$token = 'm0BM8Wgd0Kyw61i7cz7hvS0R4uF4vcgi6faFk6Ql';
// --- Here is your parameter from the http GET
$arduino_data = $_GET['arduino_data'];
// --- $arduino_data_post = $_POST['name'];
// --- Set up your Firebase url structure here
$firebasePath = '/';
/// --- Making calls
$fb = new fireBase($url, $token);
$response = $fb->push($firebasePath, $arduino_data);
sleep(2);
