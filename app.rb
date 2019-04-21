require 'sinatra'



get '/' do
  "Hello world"
end
result = exec("python3 main.py")
