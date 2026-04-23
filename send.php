<?php
declare(strict_types=1);

session_start();
mb_internal_encoding('UTF-8');

$recipients = [
    'hostel.yadirect@yandex.ru',
    'P.s.112@mail.ru',
];
$project = 'Прометей01';
$successLocation = 'thankyou.html';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit('Method Not Allowed');
}

$name = trim((string) ($_POST['name'] ?? ''));
$phone = trim((string) ($_POST['phone'] ?? ''));
$email = trim((string) ($_POST['email'] ?? ''));
$comment = trim((string) ($_POST['comment'] ?? ''));
$consent = (string) ($_POST['consent'] ?? '');
$captcha = strtoupper(trim((string) ($_POST['captcha'] ?? '')));
$formSource = trim((string) ($_POST['form_source'] ?? 'site'));
$website = trim((string) ($_POST['website'] ?? ''));

if ($website !== '') {
    http_response_code(400);
    exit('Spam detected.');
}

if ($name === '' || $phone === '') {
    http_response_code(422);
    exit('Заполните обязательные поля.');
}

if ($consent !== 'yes') {
    http_response_code(422);
    exit('Подтвердите согласие на обработку данных.');
}

$expectedCaptcha = strtoupper((string) ($_SESSION['prometej_captcha'] ?? ''));
unset($_SESSION['prometej_captcha']);

if ($expectedCaptcha === '' || $captcha === '' || $captcha !== $expectedCaptcha) {
    http_response_code(422);
    exit('Неверно введена CAPTCHA.');
}

$subject = "Новая заявка с сайта — {$project}";
$lines = [
    "Источник формы: {$formSource}",
    "Имя: {$name}",
    "Телефон: {$phone}",
    "Email: {$email}",
    "Комментарий: {$comment}",
    "Согласие: подтверждено",
    "IP: " . ($_SERVER['REMOTE_ADDR'] ?? 'unknown'),
    "User-Agent: " . ($_SERVER['HTTP_USER_AGENT'] ?? 'unknown'),
    "Дата: " . date('Y-m-d H:i:s'),
];
$message = implode("\n", $lines);

$serverName = preg_replace('/[^a-z0-9.-]+/i', '', (string) ($_SERVER['SERVER_NAME'] ?? 'localhost'));
$from = "no-reply@{$serverName}";
$headers = [];
$headers[] = 'MIME-Version: 1.0';
$headers[] = 'Content-Type: text/plain; charset=utf-8';
$headers[] = "From: {$project} <{$from}>";
$headers[] = "Reply-To: {$from}";

$ok = mail(implode(', ', $recipients), $subject, $message, implode("\r\n", $headers));

if (!$ok) {
    http_response_code(500);
    exit('Ошибка при отправке. Попробуйте позже.');
}

header("Location: {$successLocation}");
exit;
