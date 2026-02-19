<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json");

if ($_SERVER["REQUEST_METHOD"] === "OPTIONS") {
    http_response_code(204);
    exit();
}

$commentsFile = 'comments.json';
$data = json_decode(file_get_contents('php://input'), true);

$name = htmlspecialchars($data['name']);
$email = htmlspecialchars($data['email']);
$message = htmlspecialchars($data['message']);
$slug = htmlspecialchars($data['slug']);
$timestamp = date("Y-m-d H:i:s");

$newComment = [
  "name" => $name,
  "email" => $email,
  "message" => $message,
  "slug" => $slug,
  "timestamp" => $timestamp,
  "approved" => true  // auto-approved
];

$comments = [];
if (file_exists($commentsFile)) {
  $comments = json_decode(file_get_contents($commentsFile), true);
}

$comments[] = $newComment;
file_put_contents($commentsFile, json_encode($comments, JSON_PRETTY_PRINT));

echo json_encode(["status" => "success", "message" => "Comment posted successfully."]);
?>
