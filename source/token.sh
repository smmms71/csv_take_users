API=https://studio213.us/gpu
PW='ca3ouP4E'
LOGON='{"user":"mediamagic","pass":"'$PW'"}'
DATA=$(curl $API/login.php -X POST -d $LOGON)
export SES=$(echo $DATA | jq -r '.sess_id')
export SESSION=$SES
echo curl $API/reroute.php\?ses_id=$SES\&container=ubuntu -X POST -d 'ls /'
function crunjson(){ curl $API/reroute.php\?ses_id=$SES\&container=ubuntu -X POST -d $1;  }
function crun(){ OUTF=/tmp/${RANDOM}; crunjson $* >$OUTF; jq -r '.output' $OUTF;jq -r '.errors' 1>&1 $OUTF; jq -r '.files[]' $OUTF;rm $OUTF; }
echo curl $API/reroute.php\?ses_id=$SES\&container=ubuntu -X POST -d 'ls /'
function crunjson2(){ curl $API/reroute.php\?ses_id=$SES\&container=$1 -X POST -d "$2";  }
function crun2(){ OUTF=/tmp/${RANDOM}; crunjson2 $* >$OUTF; jq -r '.output' $OUTF;jq -r '.errors' 1>&1 $OUTF;jq -r '.files[]' $OUTF;rm $OUTF; }
function crun3(){ OUTF=/tmp/${RANDOM}; crunjson2 $* >$OUTF; jq -r $3 $OUTF;rm $OUTF; }