#!/usr/bin/perl

use strict;
use warnings;
use utf8;
use CGI;
use JSON;
use File::Path qw/mkpath rmtree/;

use lib qw(../../module);
use GCDebugPrint;
my $debug = GCDebugPrint->newWithJobName('chessBook/makeCategoryDir');
# $debug->{enable} = 0; # ログの出力をしない。0 eq false. デフォルトは 1。
$debug->printLog("GCDebugPrint is OK.");

$| = 1; # バッファリングしない
print "Content-type: application/json\n\n";



my $q = new CGI;
my $categoryDirName = $q->param('categoryDirName');

# 引数が空白だったら
$categoryDirName = ($categoryDirName eq '') ? 'Inbox' : $categoryDirName;

# Path 決定
my $newDirPath = "../data/PGNs/$categoryDirName";

unless (-d $newDirPath) {
  makeDir($newDirPath);
}

my @temp = glob("../data/PGNs/*");
my @dirNames = map { $_ =~ s/^.+\/([^\/]+)$/$1/; $_ } @temp;


my $json_text = encode_json( \@dirNames );
print $json_text;



sub makeDir {
    my $dirPath = shift;
    umask 0;
    mkpath( ( $dirPath ), {verbose => 0, mode => 0777} ) 
            or $debug->printLog("Dir 作成失敗: $! $dirPath");
}

1;