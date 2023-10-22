# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Release")
  file(REMOVE_RECURSE
  "CMakeFiles/MyTodo_autogen.dir/AutogenUsed.txt"
  "CMakeFiles/MyTodo_autogen.dir/ParseCache.txt"
  "MyTodo_autogen"
  )
endif()
