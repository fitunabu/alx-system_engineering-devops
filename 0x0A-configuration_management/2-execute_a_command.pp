# kills the process 'killmenow'

exec { 'pkill':
  command => '/usr/bin/pkill -9 killmenow'
}
