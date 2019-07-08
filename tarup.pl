use strict;
use warnings;
use 5.010;
use Getopt::Long qw(GetOptions);
use Data::Dumper;
use constant { true => 1, false => 0};

my @to_exclude;
my @dirs;
my $target;
my $command;

sub usage {
    say STDERR "Tar's an entire project for deployment \n";
    say STDERR "Usage: $0 [-directory DIRECTORY] [-excude DIRECTORY] \n";
    say STDERR "---------------------------------------";
    say STDERR "Required Arguments:";
    say STDERR "-t, -target           tar file name";
    say STDERR "-d, -directories      What directories to tar up";
    say STDERR "Optional Arguments:";
    say STDERR "-e, -exclude          What directories to exclude";
    say STDERR "---------------------------------------";
    say STDERR "Examples:";
    say STDERR "Usage: $0 -t my_file.tar -d dir1/";
    say STDERR "Usage: $0 -t my_file.tar -d dir1/ dir2/ dir3/ ... -e ex1/ ex2/ ex3/ ...";
    exit;
}

sub argument_join{
    my ($str, $arr, $clean) = @_;
    my @array = @{$arr};
    if($clean){
        foreach(@array){
            $_ = "\"$_\"";
        }
    }
    return $str . join(' ' . $str, @array);
}
    
GetOptions(
    'exclude=s{,}' => \@to_exclude,
    'directories=s{1,}' => \@dirs,
    'target=s' => \$target
) or usage();

if(@dirs){
    my $directories = argument_join(" ", \@dirs, false);
    $command = 'tar ';
    if (@to_exclude){
        my $excluded = argument_join("--exclude=", \@to_exclude, true);
        $command = $command . $excluded . ' -czvf ' . $target . ' ' . $directories
    } else{
        $command = $command . '-czvf ' . $target . ' ' . $directories;
    }
    system($command);
} else {
    usage();
}

