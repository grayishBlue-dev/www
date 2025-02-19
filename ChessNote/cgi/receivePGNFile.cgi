#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use File::Copy;
use File::Basename;
use lib qw(../../module);
use JSON qw/encode_json decode_json/;
use Encode qw(decode_utf8 encode_utf8);

use GCDebugPrint;
my $debug = GCDebugPrint->newWithJobName('chessBook/readPGNContent');
# $debug->{enable} = 0; # ログの出力をしない。0 eq false. デフォルトは 1。
$debug->printLog("GCDebugPrint is OK.");

$| = 1; # バッファリングしない
print "Content-type: application/json\n\n";

my $q            = new CGI;
my $categoryName = $q->param('categoryName');
my $pgnFileName  = $q->param('pgnFileName');
my $fileObj      = $q->param('file');
my $temp_path    = $q->tmpFileName($fileObj); # サーバで保管した一時ファイルのパス。


my $savePath = "../data/PGNs/$categoryName/$pgnFileName";
move ($temp_path, $savePath) || $debug->printLog("$0: can't move $savePath: $!");
chmod 0777, $savePath;

my @debug = ($categoryName, $pgnFileName, $temp_path);
$debug->printLog(\@debug);

my $jsonPretty = JSON->new->pretty();
my $jsonText = $jsonPretty->encode( \@debug );

print($jsonText);


1;
