<?php
declare(strict_types=1);

session_start();
mb_internal_encoding('UTF-8');

$recipients = [
    'hostel.yadirect@yandex.ru',
    'P.s.112@mail.ru',
];
$project = 'Прометей01';
$successLocation = '/thankyou';
$isAjax = strtolower((string) ($_SERVER['HTTP_X_REQUESTED_WITH'] ?? '')) === 'xmlhttprequest';

function respondError(int $status, string $message, bool $isAjax): void
{
    http_response_code($status);

    if ($isAjax) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode([
            'ok' => false,
            'error' => $message,
        ], JSON_UNESCAPED_UNICODE);
        exit;
    }

    exit($message);
}

function respondSuccess(string $successLocation, bool $isAjax): void
{
    if ($isAjax) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode([
            'ok' => true,
            'message' => 'Ваша заявка отправлена. В ближайшее время мы с вами свяжемся.',
        ], JSON_UNESCAPED_UNICODE);
        exit;
    }

    header("Location: {$successLocation}");
    exit;
}

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
    respondError(400, 'Spam detected.', $isAjax);
}

if ($name === '' || $phone === '') {
    respondError(422, 'Заполните обязательные поля.', $isAjax);
}

if ($consent !== 'yes') {
    respondError(422, 'Подтвердите согласие на обработку данных.', $isAjax);
}

$expectedCaptcha = strtoupper((string) ($_SESSION['prometej_captcha'] ?? ''));
unset($_SESSION['prometej_captcha']);

if ($expectedCaptcha === '' || $captcha === '' || $captcha !== $expectedCaptcha) {
    respondError(422, 'Неверно введена CAPTCHA.', $isAjax);
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
    respondError(500, 'Ошибка при отправке. Попробуйте позже.', $isAjax);
}

respondSuccess($successLocation, $isAjax);
