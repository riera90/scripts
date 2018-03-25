#/bin/zsh
printf "\n"
top_value=10
secundary_screen_brightnes_offset=1
brightness=$(calc $1 / 10)
debug=0 # [1/0]

screens=$(xrandr | sed -rn 's/^([A-Z0-9\-]*)\ connected.*/\1/p')
printf "\n Detected screens: \n"
for screen in $screens; do
	printf "\t$screen\n"
done
# exit

if [[ ${#} -lt 1 ]]; then
	echo "exit!"
  exit
fi

if [[ "$1" -lt "3" ]]; then
	printf "TO LOW!! \nUnless you want to have a nice time trying to get it back...\n"
	exit
fi
printf "\n Gloval configuration:\n"
if [[ ${#} -gt "3" ]]; then
	printf "\tSetting custom filter..."
	r=$(calc $2 / $top_value)
	g=$(calc $3 / $top_value)
	b=$(calc $4 / $top_value)
	printf " done.\n"
	if [[ "$debug" == "1" ]]; then
		echo "custom rgb"
		echo -e "r: $r"
	  echo -e "g: $g"
	 	echo -e "b: $b"
	fi
else
	if [[ "$2" == r* ]]; then
		printf "\tSetting red filter..."
	  r=1
	  g=0.7
	  b=0.5
		printf " done.\n"
		if [[ "$debug" == "1" ]]; then
			echo -e "r: $r"
		  echo -e "g: $g"
		 	echo -e "b: $b"
		fi
	else
		# echo "default rgb"
		printf "\tNothing to make.\n"
		r=1
	  g=1
	  b=1
	fi


fi
# echo $1
# xrandr --output LVDS-1 --brightness "$1"
# exit

# if [[ "$brightness" == 10 ]]; then
for screen in $screens; do
	printf "\n Changing $screen:\n"
	printf "\tapl changes..."
	xrandr --output "$screen" --brightness "$brightness" --gamma "$r":"$g":"$b"
	if [[ "$debug" == "1" ]]; then
		printf "\nDEBUG: default brightness\n"
		printf "DEBUG: xrandr --output "$screen" --brightness "$brightness" --gamma "$r":"$g":"$b""
	fi
	printf " done.\n"
done
printf "\n exito\n\n"
# else
#   echo "added brightness"
# 	xrandr --output "$main_screen" --brightness "$brightness_main" --gamma "$r":"$g":"$b"
# 	xrandr --output "$Secundary_screen" --brightness "$brightness_secundary" --gamma "$r":"$g":"$b"
# 	if [[ "$debug" == "1" ]]; then
# 		echo -e "xrandr --output "$main_screen" --brightness "$brightness_main" --gamma "$r":"$g":"$b""
# 		echo -e "xrandr --output "$Secundary_screen" --brightness "$brightness_secundary" --gamma "$r":"$g":"$b""
# 	fi
# fi
