<?php
declare(strict_types=1);

header('Content-Type: application/xml; charset=utf-8');

$siteRoot = __DIR__;
$baseUrl = 'https://prometej01.ru';

$includeExtensions = ['html', 'php'];
$excludedFiles = [
    '.htaccess',
    '.gitignore',
    '.nojekyll',
    'README.md',
    'favicon.ico',
    'send.php',
    'captcha.php',
    'thankyou.html',
];
$excludedDirectories = [
    '.git',
    'assets',
    'data',
    'photo',
    'scripts',
];

/**
 * @return array<int, array{loc: string, lastmod: string}>
 */
function collectUrls(
    string $siteRoot,
    string $baseUrl,
    array $includeExtensions,
    array $excludedFiles,
    array $excludedDirectories,
): array {
    $urls = [];

    $iterator = new RecursiveIteratorIterator(
        new RecursiveCallbackFilterIterator(
            new RecursiveDirectoryIterator($siteRoot, FilesystemIterator::SKIP_DOTS),
            static function (SplFileInfo $current) use ($excludedDirectories): bool {
                if ($current->isDir()) {
                    return !in_array($current->getFilename(), $excludedDirectories, true);
                }

                return true;
            }
        )
    );

    foreach ($iterator as $file) {
        if (!$file instanceof SplFileInfo || !$file->isFile()) {
            continue;
        }

        $relativePath = str_replace('\\', '/', substr($file->getPathname(), strlen($siteRoot) + 1));
        $filename = basename($relativePath);
        $extension = strtolower(pathinfo($relativePath, PATHINFO_EXTENSION));

        if (!in_array($extension, $includeExtensions, true)) {
            continue;
        }

        if (in_array($filename, $excludedFiles, true)) {
            continue;
        }

        $publicPath = normalizePublicPath($relativePath);

        if ($publicPath === null) {
            continue;
        }

        $urls[$publicPath] = [
            'loc' => rtrim($baseUrl, '/') . $publicPath,
            'lastmod' => gmdate('c', (int) $file->getMTime()),
        ];
    }

    ksort($urls);

    return array_values($urls);
}

function normalizePublicPath(string $relativePath): ?string
{
    $normalized = '/' . ltrim(str_replace('\\', '/', $relativePath), '/');

    if ($normalized === '/index.html') {
        return '/';
    }

    if (str_ends_with($normalized, '/index.html')) {
        return substr($normalized, 0, -10) . '/';
    }

    if (str_ends_with($normalized, '.html')) {
        return substr($normalized, 0, -5);
    }

    if (str_ends_with($normalized, '.php')) {
        return $normalized;
    }

    return null;
}

$urls = collectUrls($siteRoot, $baseUrl, $includeExtensions, $excludedFiles, $excludedDirectories);

echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
echo "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n";

foreach ($urls as $url) {
    echo "  <url>\n";
    echo '    <loc>' . htmlspecialchars($url['loc'], ENT_XML1) . "</loc>\n";
    echo '    <lastmod>' . $url['lastmod'] . "</lastmod>\n";
    echo "  </url>\n";
}

echo "</urlset>\n";
