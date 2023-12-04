include stdlib

exec { 'update packages':
  command => '/usr/bin/apt-get update',
  unless  => '/usr/bin/test -f /var/lib/apt/periodic/update-success-stamp && /usr/bin/test "$(date +%s)" -le "$(( $(date --date="$(cat /var/lib/apt/periodic/update-success-stamp)" +%s) + 86400 ))"',
}

package { 'nginx':
  ensure => installed,
  require => Exec['update packages'],
}

file { '/var/www/html/index.html':
  ensure  => 'present',
  content => 'Hello World!',
  mode    => '0644',
  owner   => 'root',
  group   => 'root',
}

file_line { 'nginx_server_name':
  path => '/etc/nginx/sites-enabled/default',
  line => "\tserver_name _;",
  match => '^\\s*server_name',
}

file_line { 'nginx_redirect':
  path => '/etc/nginx/sites-enabled/default',
  line => "\trewrite ^/redirect_me https://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;",
  after => '^\\s*server_name',
  require => File_line['nginx_server_name'],
}

file { '/var/www/html/404.html':
  ensure  => 'file',
  content => "Ceci n'est pas une page",
  require => Package['nginx'],
}

exec { 'add_custom_header':
  command => "sed -i '/server_name _;/a add_header X-Served-By \$HOSTNAME;' /etc/nginx/sites-enabled/default",
  path    => ['/bin', '/usr/bin', '/usr/sbin'],
  require => Package['nginx'],
}

exec { 'nginx_test':
  command => 'nginx -t',
  path    => ['/bin', '/usr/bin', '/usr/sbin'],
  require => Exec['add_custom_header'],
}

service { 'nginx':
  ensure  => running,
  enable  => true,
}