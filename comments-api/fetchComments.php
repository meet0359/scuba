<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

$commentsFile = 'comments.json';

if (!file_exists($commentsFile)) {
  echo json_encode([]);
  exit;
}

$slug = $_GET['slug'] ?? '';
$comments = json_decode(file_get_contents($commentsFile), true);

$filtered = array_filter($comments, function ($comment) use ($slug) {
  return isset($comment['slug']) &&
         $comment['slug'] === $slug &&
         $comment['approved'] == true; // ✅ Loose comparison
});

echo json_encode(array_values($filtered));
?>
