#!/usr/bin/perl

use strict;
use warnings;
use utf8;
# use open ":utf8";
# use open ":std";
use CGI;
use JSON qw/encode_json decode_json/;
use Encode qw(decode_utf8 encode_utf8);
use File::Path qw/mkpath rmtree/;
use lib qw(../../module);
# use lib qw(../../../module); # 開発環境での perl -c チェック時。


use GCDebugPrint;
my $debug = GCDebugPrint->newWithJobName('chessBook/readWriteAnnotation');
# $debug->{enable} = 0; # ログの出力をしない。0 eq false. デフォルトは 1。
$debug->printLog("GCDebugPrint is OK.");

my $q        = new CGI;
my $mode     = $q->param('mode');
my $dirName  = $q->param('categoryName');
my $fileName = $q->param('fileName');
my $value    = $q->param('annoValue');
my $annoKey  = $q->param('annoKey'); # write mode only
my $target  = $q->param('target');

utf8::decode($dirName);
utf8::decode($fileName);
utf8::decode($value);
utf8::decode($annoKey);
utf8::decode($target);
my $argv = "Recived: $mode / $annoKey / $value / $dirName / $fileName / $target";
$debug->printLog($argv);

my $filePath = '';
if ($target eq 'private') {
    $fileName =~ s/(.+)\.pgn$/$1\.txt/;
    $filePath = "../data/annotations/$dirName/$fileName";
}
else {
    $filePath = "../data/PGNs/$dirName/$fileName";
}
$debug->printLog("anno file path: $filePath");


$| = 1; # バッファリングしない
print "Content-type: application/json\n\n";

my %result;
my $json_text = '';

if (-f $filePath) {
    $json_text = get_content($filePath);
}

if ($mode eq 'write') {
    if ($target eq 'private') {
        my $json = writeAnno($filePath, $json_text, $annoKey, $value);
        $json_text = encode_json( $json );
    }
    elsif ($mode eq 'public'){
        my $json = writeComment($filePath, $annoKey, $value);
        $json_text = encode_json( $json );
    }
}

print $json_text;








# --------------------------------------------

sub writeAnno{
    my $filePath = shift;
    my $json_text = shift;
    my $annoKey = shift;
    my $value = shift;
    my $jsonData = [];

    if ($json_text ne '') {
        $debug->printLog('defined $json_text');
        $jsonData = decode_json( $json_text );
    }
    else{
        # ディレクトリをチェック
        my $log_dir = "../data/annotations/${dirName}";
        unless (-d $log_dir) {
            umask 0;
            mkpath( $log_dir, {verbose => 0, mode => 0777} ) or $debug->printLog($!);
        }

        my %newAnnotation = ();
        $jsonData = \%newAnnotation;
    }

    $jsonData->{$annoKey} = $value;
    my $json = encode_json($jsonData);
    put_content($filePath, $json);

    return $jsonData;
}


sub writeComment{
    my $filePath = shift;
    my $annoKey = shift;
    my $value = shift;
    my $jsonData = [];

    my $log = "writeComment: $filePath, $annoKey, $value";
    $debug->printLog($log);

    if( -f $filePath ) {
        my $content = get_content($filePath);
        my @lines = split(/\n/, $content);
        
        my @sevenTagRoster = ();
        my @moveList = ();
        foreach my $row (@lines) {
            if ($row =~ /^ *\[/ or $row =~ /^ *$/) {
                push(@sevenTagRoster, $row);
                next;
            }
            push(@moveList, $row);
        }

        my $stream = '';
        foreach my $row (@moveList) {
            $stream .= " $row";
        }

        my @numberIndex = ();
        @numberIndex = $stream =~ m/\d{1,3}\./g;

        my @moves = split(/ *\d{1,3}\. */, $stream);

        # 検証
        my $numL = @numberIndex;
        my $moveL = @moves;
        unless ($numL == ($moveL -1)) {
            $debug->printLog('move 分解失敗。');
            $debug->printLog($stream); $debug->printLog(\@sevenTagRoster); $debug->printLog(\@numberIndex); $debug->printLog(\@moves);
            return;
        }

        my $index = $annoKey;
        $index =~ s/[^\d]//g;
        --$index;
        $debug->printLog("numberIndex[$index] : $moves[$index]");

        my @block = $moves[$index] =~ /([^{} ]+|{[^}]+})/g;
        $debug->printLog(\@block);




    }
    else{
        $debug->printLog("did’t find ${filePath}.");
    }

    return $jsonData;
}



# ファイルの内容を取得する関数
sub get_content {
    my $file = shift;
    open(FH_IN, "<", $file) or die $debug->printLog("$file : $!");
        my $content = do { local $/; <FH_IN> };
    close FH_IN;
    return $content;
}

sub put_content {
    my $file = shift;
    my $content = shift;
    open(FH_OUT, "> $file") or die $debug->printLog("$file : $!");
        print FH_OUT $content;
    close FH_OUT;
}

1;
