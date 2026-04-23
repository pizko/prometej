<?php
declare(strict_types=1);

session_start();

$chars = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ';
$code = '';
for ($i = 0; $i < 5; $i++) {
    $code .= $chars[random_int(0, strlen($chars) - 1)];
}

$_SESSION['prometej_captcha'] = $code;

header('Content-Type: image/svg+xml; charset=UTF-8');
header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');

$noise = '';
for ($i = 0; $i < 6; $i++) {
    $x1 = random_int(0, 180);
    $y1 = random_int(0, 56);
    $x2 = random_int(0, 180);
    $y2 = random_int(0, 56);
    $noise .= sprintf(
        '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="rgba(223,31,38,0.25)" stroke-width="1.5" />',
        $x1, $y1, $x2, $y2
    );
}

$letters = '';
$x = 18;
for ($i = 0; $i < strlen($code); $i++) {
    $char = $code[$i];
    $y = random_int(34, 42);
    $rotate = random_int(-10, 10);
    $letters .= sprintf(
        '<text x="%d" y="%d" transform="rotate(%d %d %d)" font-family="Arial, sans-serif" font-size="26" font-weight="700" fill="#111826">%s</text>',
        $x, $y, $rotate, $x, $y, htmlspecialchars($char, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8')
    );
    $x += 30;
}

echo <<<SVG
<svg xmlns="http://www.w3.org/2000/svg" width="180" height="56" viewBox="0 0 180 56" fill="none">
  <rect width="180" height="56" rx="12" fill="#F8FAFC"/>
  <rect x="1" y="1" width="178" height="54" rx="11" stroke="#D7DFEA"/>
  {$noise}
  {$letters}
</svg>
SVG;
