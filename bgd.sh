#/bin/zsh
top_value=10
secundary_screen_brightnes_offset=1
brightness_main=$(calc $1 / 10)
brightness_secundary=$(calc $(calc $1 / $top_value) + $(calc $secundary_screen_offset / $top_value ))
main_screen=LVDS-1
Secundary_screen=VGA-1-2
debug=0 # [1/0]

if [[ ${#} -lt 1 ]]; then
	echo "exit!"
  exit
fi

if [[ "$1" -lt "3" ]]; then
	printf "TO LOW!! \nUnless you want to have a nice time trying to get it back...\n"
	exit
fi

if [[ ${#} -gt "3" ]]; then
	printf "\tSetting custom filter..."
	r=$(clac $2 / $top_value)
	g=$(clac $3 / $top_value)
	b=$(clac $4 / $top_value)
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
		r=1
	  g=1
	  b=1
	fi

fi
# echo $1
# xrandr --output LVDS-1 --brightness "$1"
# exit

# if [[ "$brightness" == 10 ]]; then
	printf "\tapl changes..."
	xrandr --output "$main_screen" --brightness "$brightness_main" --gamma "$r":"$g":"$b"
	xrandr --output "$Secundary_screen" --brightness "$brightness_secundary" --gamma "$r":"$g":"$b"
	if [[ "$debug" == "1" ]]; then
		echo "default brightness"
		printf "\n"
		echo -e "xrandr --output "$main_screen" --brightness "$brightness_main" --gamma "$r":"$g":"$b""
		echo -e "xrandr --output "$Secundary_screen"1 --brightness "$brightness_secundary" --gamma "$r":"$g":"$b""
	fi
	printf " done.\n"

# else
#   echo "added brightness"
# 	xrandr --output "$main_screen" --brightness "$brightness_main" --gamma "$r":"$g":"$b"
# 	xrandr --output "$Secundary_screen" --brightness "$brightness_secundary" --gamma "$r":"$g":"$b"
# 	if [[ "$debug" == "1" ]]; then
# 		echo -e "xrandr --output "$main_screen" --brightness "$brightness_main" --gamma "$r":"$g":"$b""
# 		echo -e "xrandr --output "$Secundary_screen" --brightness "$brightness_secundary" --gamma "$r":"$g":"$b""
# 	fi
# fi
