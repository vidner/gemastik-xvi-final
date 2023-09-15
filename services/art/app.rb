require "sinatra"
require "slim"

set :port, 8080
set :bind, '0.0.0.0'
set :environment, :production

get '/' do
    redirect '/art/gemastik'
end

get '/art/:word' do
    return Slim::Template.new{ '<iframe height="100%" width="100%" frameborder="0" src=https://asciified.thelicato.io/api/v2/ascii?text=' + params[:word] + '></iframe>' }.render
end