c
  package { 'nginx':
    ensure => installed,
  }

  file { '/var/www/html/index.html':
    ensure  => file,
    content => 'Hello World!',
    require => Package['nginx'],
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
    ensure  => file,
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
    require => Exec['nginx_test'],
  }
}
