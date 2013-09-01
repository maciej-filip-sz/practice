#!/usr/bin/env watchr

# config file for watchr http://github.com/mynyml/watchr
# install: gem install watchr
# run: watch watchr.rb
# note: make sure that you have jstd server running (server.sh) and a browser captured

log_file = File.expand_path(File.dirname(__FILE__) + '/../logs/renderer.log')

`cd ..`
`touch #{log_file}`

puts "String watchr... log file: #{log_file}"

watch( 'projects/.*\.yaml' ) {
  |md|
  fname = File.basename(md.to_s())
  name = fname.chomp(File.extname(fname))
  `echo "\n\nbuild run started @ \`date\`" > #{log_file}`
  puts "Rendering project #{md}."
  `scripts/render_project.py projects #{fname} templates/project.template > app/#{name}.html`
}

watch( 'templates/project.template' ) {
  |md|
  `echo "\n\nbuild run started @ \`date\`" > #{log_file}`
  puts "Rendering all projects with new template."
  Dir.glob('projects/*.yaml') do |fname|
    fname = File.basename(fname)
    name = fname.chomp(File.extname(fname))
    `scripts/render_project.py projects #{fname} templates/project.template > app/#{name}.html`
  end
}