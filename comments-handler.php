<?php
$rawData = file_get_contents("php://input");
$data = json_decode($rawData, true);

if (!$data || !isset($data['name'], $data['email'], $data['text'], $data['slug'])) {
  http_response_code(400);
  echo "Invalid input.";
  exit;
}

$entry = implode(" | ", [
  date("Y-m-d H:i:s"),
  $data['slug'],
  $data['name'],
  $data['email'],
  str_replace(["\r", "\n"], " ", $data['text'])
]);

file_put_contents("comments.txt", $entry . PHP_EOL, FILE_APPEND);
echo "Success";
