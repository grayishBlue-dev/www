#!/usr/bin/perl

use strict;
use warnings;
use utf8;
use CGI;
use JSON;
use Encode qw(decode_utf8 encode_utf8);
use Encode::Guess qw(cp932 utf8);
use File::Path qw/mkpath rmtree/;
use lib qw(../../module);


use GCDebugPrint;
my $debug = GCDebugPrint->newWithJobName('chessBook/readPGNContent');
# $debug->{enable} = 0; # ログの出力をしない。0 eq false. デフォルトは 1。
$debug->printLog("GCDebugPrint is OK.");

my $q    = new CGI;
my $dirName = $q->param('dirName');
my $fileName = $q->param('fileName');
my $filePath = "../data/PGNs/${dirName}/${fileName}";

$| = 1; # バッファリングしない
print "Content-type: application/json\n\n";

my @result = ();
if (-f $filePath) {
  my ($fh_in, $error, $enc) = open_binary4read($filePath);
  while(my $aValue = <$fh_in>){
      utf8::decode($aValue);
      chomp($aValue);
      # if($aValue =~ /^$/) { next };
      push( @result, $aValue );
  }
  close($fh_in);
}
else{
  push( @result, "There is not $filePath" );
}

my $json_text = encode_json( \@result );
$debug->printLog(\@result);
print $json_text;


sub open_binary4read {
	my $file = shift;

	#引数チェック
	$file and -f $file
		or return (undef, 'File path not set or file does not exists.');

	my $fh;
	unless (open ($fh, '<:raw', $file)){
		return(undef, "OPEN FAILED: $file, $!");
	}

	my ($temp, $i);
	while ($temp .= <$fh> and ++$i < 20){
		eof and last;
	}
	close ($fh);
	my $genc = guess_encoding($temp);

	# Perlでのエンコーディング指定を取得。判別できない場合のデフォルトを指定
	my $enc = eval{$genc->name} || 'utf8';

	unless (open ($fh, "<:encoding($enc)", $file)){
		return(undef, "OPEN FAILED: $file, $!");
	}
	return ($fh, undef, $enc);
}

1;



