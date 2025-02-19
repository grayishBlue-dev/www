#!/usr/bin/perl

use strict;
use warnings;
use utf8;
use CGI;
use JSON;
use Encode qw(decode_utf8 encode_utf8);
use File::Path qw/mkpath rmtree/;
use lib qw(../../module);

use GCDebugPrint;
my $debug = GCDebugPrint->newWithJobName('chessBook/readDirName');
# $debug->{enable} = 0; # ログの出力をしない。0 eq false. デフォルトは 1。
$debug->printLog("GCDebugPrint is OK.");

my $result = '';

my $q    = new CGI;
my $mode = $q->param('mode');

$| = 1; # バッファリングしない
print "Content-type: application/json\n\n";

my @temp = glob("../data/PGNs/*");
my @files = map { $_ =~ s/^.+\/([^\/]+)$/$1/; $_ } @temp;

$debug->printLog(\@files);

my $json_text = encode_json( \@files );
print $json_text;

1;
