case "$1" in
  
  build)
    docker-compose up --force-recreate --build --no-start app
    ;;

  cleanup)
    docker-compose -f docker-compose.yml -f down -v
    ;;

  scrap)
    docker-compose up -d postgres
    export APP_ACTION='scrap'
    export APP_PARAM="$2"
    docker-compose up app
    ;;

  report)
    docker-compose up -d postgres
    export APP_ACTION='report'
    export APP_PARAM="$2"
    docker-compose up app
    ;;


  *)
    echo "Usage: run.sh {scrap|report|cleanup}"
    echo "  -scrap: run scrapper, will scrap Reuters feed (hardcoded), db with schema will be provided automatically."
    echo "  -report <YYYY-DD-MM>: output news for given date into news-YYYY-DD-MM.csv (delimiter ;) into current dir."
    echo "  -cleanup: stop all services and remove database data. USE CAREFULLY!"

esac
