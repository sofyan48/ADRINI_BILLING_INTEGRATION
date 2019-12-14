# ADRINI BILLING INTEGRATION FOR ADRINI

## INSTALLING

Copy env.example to .env
```
cp env.example .env
```
setting your environment

```
pip install -r requirements.txt
```

## DATABASE
Installing CockroachDB Reference [action](https://www.cockroachlabs.com/docs/stable/deploy-cockroachdb-on-premises-insecure.html)
if you need sql file please contact me : meongbego@gmail.com

## DEVELOPMENT

```
python manager.py server
```

## PRODUCTION
using gunicorn run
```
sh run.sh
```

## BILLING
Use : Invoice ninja [action](https://www.invoiceninja.com/)