require 'sinatra'


result = exec("python3 main.py")

get '/' do
  "Hello world"
end
