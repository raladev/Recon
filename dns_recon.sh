#!/bin/sh

#Tools pathes
AMASS_PATH=${HOME}/tools/amass_v3.4.2_linux_amd64
MASSDNS_PATH=${HOME}/tools/massdns
PROJECTS_FOLDER=${HOME}/myProjects

run_for_only_one_domain(){
	echo "domain is $domain and project is $project"
	
	domain_folder="${PROJECTS_FOLDER}/${project}/${domain}"
	mkdir -p ${domain_folder}
	
	if [ "${scan_mode}" == "full" ]; then		

		#PASSIVE SCAN

		#Amass scan(passive_out.txt)
		echo "Amass passive scan with config"
		${AMASS_PATH}/amass enum --passive  -v -noalts -exclude commoncrawl -config ${AMASS_PATH}/config.ini -o ${domain_folder}/passive_out.txt -log ${domain_folder}/amass.log -d ${domain} 

		#Resolve passive scan(resolved_passive.txt)
		echo "DNS resolving for amass + rapid7"
		${MASSDNS_PATH}/bin/massdns -r data/public_dns.txt -q -t A -o S -w ${domain_folder}/resolved_passive.txt ${domain_folder}/passive_out.txt

		#Save unresolved for vhost brute (unresolved_passive.txt)
		echo "Saving unresolved create_domain_list_for_alt"
		python3 sub_scripts/create_unresolved_list.py ${domain_folder} ${domain_folder}/passive_out.txt ${domain_folder}/resolved_passive.txt

		#BRUTEFORCE

		#Bruteforce list creation(brute_list.txt)
		echo "Brutefoce list creation"
		python3 sub_scripts/create_brute_dns_list.py data/subdomains_for_bruteforce.txt ${domain_folder} ${domain}

		#Resolve brute list(resolved_brute.txt)
		echo "DNS resolving for brute list"
		${MASSDNS_PATH}/bin/massdns -r data/public_dns.txt -q -t A -o S -w ${domain_folder}/resolved_brute.txt ${domain_folder}/brute_list.txt
		rm ${domain_folder}/brute_list.txt

		#Brute vhost (for now only unresolved output of passive scan is used for the vhost brute)

		#ALTERATIONS BRUTEFORCE

		#alterations creation (resolved_passive + resolved+brute = domains_for_alt.txt, domains_for_alt.txt -> alt_list.txt)
		echo "Alterations creation"
		python3 sub_scripts/create_domain_list_for_alt.py ${domain_folder} ${domain_folder}/resolved_passive.txt ${domain_folder}/resolved_brute.txt
		dnsgen ${domain_folder}/domains_for_alt.txt > ${domain_folder}/alt_list.txt

		#Resolve alt list(resolved_alt.txt)
		echo "DNS resolving for alt list"
		${MASSDNS_PATH}/bin/massdns -r data/public_dns.txt -q -t A -o S -w ${domain_folder}/resolved_alt.txt ${domain_folder}/alt_list.txt
		rm ${domain_folder}/domains_for_alt.txt
		rm ${domain_folder}/alt_list.txt
		
		#FINAL SUBDOMAIN REPORT
		
		#Build final list of subdomains(fin_only_domains.txt, fin_statistic.txt, fin_a_dns_records.txt)
		echo "Fin report creation"
		python3 sub_scripts/create_fin_report.py ${domain_folder} ${domain_folder}/resolved_passive.txt ${domain_folder}/resolved_brute.txt ${domain_folder}/resolved_alt.txt

	elif [ "${scan_mode}" == "scedule_scan" ]; then		
		echo "Section under construction"
	fi

	echo "End of domain scan"
}

run_for_file(){
	echo "file is $file"
	while IFS= read -r line
    do
        domain="$line"
        run_for_only_one_domain 
    done < "$file"
    echo "End of domainS scan"
}

while getopts d:f:p:m: option
do
	case "${option}"
	in
	d) domain=${OPTARG};;
	f) file=${OPTARG};;
	p) project=${OPTARG};;
	m) scan_mode=${OPTARG};;
	esac
done

if [ -n "$domain" ] && [ -n "$file" ]; then
   echo "You need choose domain or file option"
   exit 1
elif [ -z "$domain" ] && [ -z "$file" ] || [ -z "$project" ]; then
   echo "One of parameters is required:"
   echo "-d domain - domain for enumeration OR -f file - file with list of domains for enum"
   echo "-p project name"
   exit 1
elif [ -n "$domain" ]; then
	run_for_only_one_domain
elif [ -n "$file" ]; then
	run_for_file
fi
