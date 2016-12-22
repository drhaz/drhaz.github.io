echo "Parsing though directory $1"

list=`ls $1/*.jpg | grep -vwE "150x150"`


for image in $list
do
 thumb=`echo $image | sed s/\.jpg/-150x150\.jpg/` 
 echo "<a class=\"example-image-link\" href=\"${image}\" data-lightbox=\"animals\" data-title=\"My caption\"><img src=\"${thumb}\"/></a>"
done
