import requests
import re
url = 'https://dsbs.sba.gov/search/dsp_profilelist.cfm?RequestTimeout=180'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'CFID=11070; CFTOKEN=d6283bfe076b5dfd-2BEF4446-D8DC-FBD9-425580ACC360663B; JSESSIONID=71C7C1BCDA6F24A30D6939A2F123E24A.cfusion; PageLoadTime=1730529397206; AWSALB=Cr2KaBuCK+pNSqiK3tauGGvfY7B3BhjWXfUXQsxC5ETIuU1dQXaZx7uDUkXjMI58j9DTPc9gxQO47LrtUcZ5hE9kawV5wj8+d8tlFJyVJRRZKkH4+360t0y/OleO; AWSALBCORS=Cr2KaBuCK+pNSqiK3tauGGvfY7B3BhjWXfUXQsxC5ETIuU1dQXaZx7uDUkXjMI58j9DTPc9gxQO47LrtUcZ5hE9kawV5wj8+d8tlFJyVJRRZKkH4+360t0y/OleO',
    'origin': 'https://dsbs.sba.gov',
    'priority': 'u=0, i',
    'referer': 'https://dsbs.sba.gov/search/dsp_dsbs.cfm',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

data = {
    'CameFromQuickSearch': 'No',
    'CameFromSearchHubzone': 'No',
    'CameFromSearchTMOnLine': 'No',
    'JavaScriptOn': 'No',
    'MightNotGetSent': 'Agr,Anemp,AnyAllGreen,AnyAllKeywords,AnyAllNaics,Area,AtLeastNoMore,CageCd,Cbona,Cbonc,CBT,Cdist,Cnty,CntyNm,CompanyName,CompanyNameSearch,CompanyUserId,Dbe,Delimiter,Dunses,E8a,E8acase,Edi,Edw,Edwosb,Ein,ExpCountry,ExpMainAct,ExpMrkt,ExportCd,FirmListColumns,FirmListColumnNamesHidden,FontSize,Gcc,Greens,Gsa,HubCert,InTMO,KeyWhere,Keywords,Mntr,Msa,Naicses,NumberOfRows,Password,Phone,PIM,Qas,Report,SaveDBHits,SbaDsn,SbaOffice,SbaSbc,Sbona,Sbonc,Sdb,SearchDB,Seckp,Secst,ShowRandomizer,Sics,Sort,State,Status,Suffix,Technet,Updated,UpdBefAft,UEI,UseOracle,Uscit,UserId,Wob,Wosb,VetSB,VetSerDis,Zip,DispAnyAllComment,DispAnyAllMSIE,DispDisclaimer,DispSectionLocation,DispSectionCertifications,DispSectionOwnership,DispSectionNaicsAndKeywords,DispSectionAreaAndTechnet,DispSectionUpdated,DispSectionBonding,DispSectionQas,DispSectionSize,DispSectionCapabilities,DispSectionSpecificFirm,DispSectionPrivSearch,DispSectionDisplayOptions',
    'PageNames': 'dsp_dsbs.cfm,dsp_profilelist.cfm,dsp_profile.cfm',
    'PathNames': '/search,/pro-net/search,/dsbs/search,/dsbs',
    'PIM': 'P',
    'SearchDB': 'SBA',
    'StartRow': '1',
    'StartTimeOfSearch': '',
    'State': '',
    'Cdist': '',
    'Cnty': '',
    'CntyNm': '',
    'Phone': '',
    'Msa': '',
    'SbaOffice': '',
    'Zip': '',
    'E8a': 'N',
    'wosb': 'N',
    'HubCert': 'N',
    'edwosb': 'N',
    'vetsb': 'N',
    'vetserdis': 'N',
    'AnyAllNaics': 'Any',
    'Naicses': '',
    'AnyAllGreen': 'Any',
    'Greens': '',
    'AnyAllKeywords': 'Any',
    'Keywords': '',
    'KeyWhere': 'O',
    'Area': '',
    'Cbonc': '',
    'Cbona': '',
    'Sbonc': '',
    'Sbona': '',
    'AtLeastNoMore': 'N',
    'Anemp': '',
    'Agr': '',
    'Gcc': 'N',
    'Gsa': 'N',
    'ExportCd': 'N',
    'CageCd': '',
    'UEI': '',
    'E8acase': '',
    'CompanyName': '',
    'CompanyNameSearch': 'F',
    'UpdBefAft': 'A',
    'Updated': '',
    'Status': ['A', ''],
    'NumberOfRows': '99999999',
    'FirmListColumns': 'I01,I37,I35,P01,I11,I12',
    'FirmListColumnNamesHidden': 'Name of Firm;Contact;Address and City, State Zip;Capabilities Narrative;E-mail Address;WWW Page URL',
    'FirmListColumnNamesDisplay': 'Name of Firm; Contact; Address and City, State Zip; Capabilities Narrative; E-mail Address; WWW Page URL',
    'FontSize': '10pt',
    'Suffix': 'xls',
    'Report': 'M',
    'Delimiter': 'C',
    'Submit': 'Search Using These Criteria'
}

state_fails = []

def get_state_data(state, area, cnty = ''):
    data["State"] = state
    data["Area"] = area
    data["Cnty"] = cnty

    response = requests.post(url, headers=headers, data=data)
    file_name = f"data/{state}_{area}_{cnty}_data.html"

    if response.status_code == 200:
        print("Request successful")
        with open(file_name, 'wb') as f:
            f.write(response.content)
    else:
        state_fails.append(state)
        print(f"Request failed with status code: {response.status_code}")


us_states = [
    ("Alabama", "AL"),
    ("Alaska", "AK"),
    ("Arizona", "AZ"),
    ("Arkansas", "AR"),
    ("California", "CA"),
    ("Colorado", "CO"),
    ("Connecticut", "CT"),
    ("Delaware", "DE"),
    ("Florida", "FL"),
    ("Georgia", "GA"),
    ("Hawaii", "HI"),
    ("Idaho", "ID"),
    ("Illinois", "IL"),
    ("Indiana", "IN"),
    ("Iowa", "IA"),
    ("Kansas", "KS"),
    ("Kentucky", "KY"),
    ("Louisiana", "LA"),
    ("Maine", "ME"),
    ("Maryland", "MD"),
    ("Massachusetts", "MA"),
    ("Michigan", "MI"),
    ("Minnesota", "MN"),
    ("Mississippi", "MS"),
    ("Missouri", "MO"),
    ("Montana", "MT"),
    ("Nebraska", "NE"),
    ("Nevada", "NV"),
    ("New Hampshire", "NH"),
    ("New Jersey", "NJ"),
    ("New Mexico", "NM"),
    ("New York", "NY"),
    ("North Carolina", "NC"),
    ("North Dakota", "ND"),
    ("Ohio", "OH"),
    ("Oklahoma", "OK"),
    ("Oregon", "OR"),
    ("Pennsylvania", "PA"),
    ("Rhode Island", "RI"),
    ("South Carolina", "SC"),
    ("South Dakota", "SD"),
    ("Tennessee", "TN"),
    ("Texas", "TX"),
    ("Utah", "UT"),
    ("Vermont", "VT"),
    ("Virginia", "VA"),
    ("Washington", "WA"),
    ("West Virginia", "WV"),
    ("Wisconsin", "WI"),
    ("Wyoming", "WY")
]
areas = ['MFG', 'CON' ,'RAD', 'SVC']
ca_counties = '(any county)</option><option value="001">001 - ALAMEDA</option><option value="003">003 - ALPINE</option><option value="005">005 - AMADOR</option><option value="007">007 - BUTTE</option><option value="009">009 - CALAVERAS</option><option value="011">011 - COLUSA</option><option value="013">013 - CONTRA COSTA</option><option value="015">015 - DEL NORTE</option><option value="017">017 - EL DORADO</option><option value="019">019 - FRESNO</option><option value="021">021 - GLENN</option><option value="023">023 - HUMBOLDT</option><option value="025">025 - IMPERIAL</option><option value="027">027 - INYO</option><option value="029">029 - KERN</option><option value="031">031 - KINGS</option><option value="033">033 - LAKE</option><option value="035">035 - LASSEN</option><option value="037">037 - LOS ANGELES</option><option value="039">039 - MADERA</option><option value="041">041 - MARIN</option><option value="043">043 - MARIPOSA</option><option value="045">045 - MENDOCINO</option><option value="047">047 - MERCED</option><option value="049">049 - MODOC</option><option value="051">051 - MONO</option><option value="053">053 - MONTEREY</option><option value="055">055 - NAPA</option><option value="057">057 - NEVADA</option><option value="059">059 - ORANGE</option><option value="061">061 - PLACER</option><option value="063">063 - PLUMAS</option><option value="065">065 - RIVERSIDE</option><option value="067">067 - SACRAMENTO</option><option value="069">069 - SAN BENITO</option><option value="071">071 - SAN BERNARDINO</option><option value="073">073 - SAN DIEGO</option><option value="075">075 - SAN FRANCISCO</option><option value="077">077 - SAN JOAQUIN</option><option value="079">079 - SAN LUIS OBISPO</option><option value="081">081 - SAN MATEO</option><option value="083">083 - SANTA BARBARA</option><option value="085">085 - SANTA CLARA</option><option value="087">087 - SANTA CRUZ</option><option value="089">089 - SHASTA</option><option value="091">091 - SIERRA</option><option value="093">093 - SISKIYOU</option><option value="095">095 - SOLANO</option><option value="097">097 - SONOMA</option><option value="099">099 - STANISLAUS</option><option value="101">101 - SUTTER</option><option value="103">103 - TEHAMA</option><option value="105">105 - TRINITY</option><option value="107">107 - TULARE</option><option value="109">109 - TUOLUMNE</option><option value="111">111 - VENTURA</option><option value="113">113 - YOLO</option><option value="115">115 - YUBA</option></select>'
va_counties = '(any county)</option><option value="001">001 - ACCOMACK</option><option value="003">003 - ALBEMARLE</option><option value="510">510 - ALEXANDRIA CITY</option><option value="005">005 - ALLEGHANY</option><option value="007">007 - AMELIA</option><option value="009">009 - AMHERST</option><option value="011">011 - APPOMATTOX</option><option value="013">013 - ARLINGTON</option><option value="015">015 - AUGUSTA</option><option value="017">017 - BATH</option><option value="019">019 - BEDFORD</option><option value="021">021 - BLAND</option><option value="023">023 - BOTETOURT</option><option value="520">520 - BRISTOL</option><option value="025">025 - BRUNSWICK</option><option value="027">027 - BUCHANAN</option><option value="029">029 - BUCKINGHAM</option><option value="530">530 - BUENA VISTA CITY</option><option value="031">031 - CAMPBELL</option><option value="033">033 - CAROLINE</option><option value="035">035 - CARROLL</option><option value="036">036 - CHARLES CITY</option><option value="037">037 - CHARLOTTE</option><option value="540">540 - CHARLOTTESVILLE CITY</option><option value="550">550 - CHESAPEAKE CITY</option><option value="041">041 - CHESTERFIELD</option><option value="043">043 - CLARKE</option><option value="570">570 - COLONIAL HEIGHTS CITY</option><option value="580">580 - COVINGTON CITY</option><option value="045">045 - CRAIG</option><option value="047">047 - CULPEPER</option><option value="049">049 - CUMBERLAND</option><option value="590">590 - DANVILLE CITY</option><option value="051">051 - DICKENSON</option><option value="053">053 - DINWIDDIE</option><option value="057">057 - ESSEX</option><option value="059">059 - FAIRFAX</option><option value="600">600 - FAIRFAX CITY</option><option value="610">610 - FALLS CHURCH CITY</option><option value="061">061 - FAUQUIER</option><option value="063">063 - FLOYD</option><option value="065">065 - FLUVANNA</option><option value="067">067 - FRANKLIN</option><option value="620">620 - FRANKLIN CITY</option><option value="069">069 - FREDERICK</option><option value="630">630 - FREDERICKSBURG CITY</option><option value="640">640 - GALAX CITY</option><option value="071">071 - GILES</option><option value="073">073 - GLOUCESTER</option><option value="075">075 - GOOCHLAND</option><option value="077">077 - GRAYSON</option><option value="079">079 - GREENE</option><option value="081">081 - GREENSVILLE</option><option value="083">083 - HALIFAX</option><option value="650">650 - HAMPTON CITY</option><option value="085">085 - HANOVER</option><option value="660">660 - HARRISONBURG CITY</option><option value="087">087 - HENRICO</option><option value="089">089 - HENRY</option><option value="091">091 - HIGHLAND</option><option value="670">670 - HOPEWELL CITY</option><option value="093">093 - ISLE OF WIGHT</option><option value="095">095 - JAMES CITY</option><option value="097">097 - KING AND QUEEN</option><option value="099">099 - KING GEORGE</option><option value="101">101 - KING WILLIAM</option><option value="103">103 - LANCASTER</option><option value="105">105 - LEE</option><option value="678">678 - LEXINGTON CITY</option><option value="107">107 - LOUDOUN</option><option value="109">109 - LOUISA</option><option value="111">111 - LUNENBURG</option><option value="680">680 - LYNCHBURG CITY</option><option value="113">113 - MADISON</option><option value="683">683 - MANASSAS CITY</option><option value="685">685 - MANASSAS PARK CITY</option><option value="690">690 - MARTINSVILLE CITY</option><option value="115">115 - MATHEWS</option><option value="117">117 - MECKLENBURG</option><option value="119">119 - MIDDLESEX</option><option value="121">121 - MONTGOMERY</option><option value="125">125 - NELSON</option><option value="127">127 - NEW KENT</option><option value="700">700 - NEWPORT NEWS CITY</option><option value="710">710 - NORFOLK CITY</option><option value="131">131 - NORTHAMPTON</option><option value="133">133 - NORTHUMBERLAND</option><option value="720">720 - NORTON CITY</option><option value="135">135 - NOTTOWAY</option><option value="137">137 - ORANGE</option><option value="139">139 - PAGE</option><option value="141">141 - PATRICK</option><option value="730">730 - PETERSBURG CITY</option><option value="143">143 - PITTSYLVANIA</option><option value="735">735 - POQUOSON CITY</option><option value="740">740 - PORTSMOUTH CITY</option><option value="145">145 - POWHATAN</option><option value="147">147 - PRINCE EDWARD</option><option value="149">149 - PRINCE GEORGE</option><option value="153">153 - PRINCE WILLIAM</option><option value="155">155 - PULASKI</option><option value="750">750 - RADFORD</option><option value="157">157 - RAPPAHANNOCK</option><option value="159">159 - RICHMOND</option><option value="760">760 - RICHMOND CITY</option><option value="161">161 - ROANOKE</option><option value="770">770 - ROANOKE CITY</option><option value="163">163 - ROCKBRIDGE</option><option value="165">165 - ROCKINGHAM</option><option value="167">167 - RUSSELL</option><option value="775">775 - SALEM</option><option value="169">169 - SCOTT</option><option value="171">171 - SHENANDOAH</option><option value="173">173 - SMYTH</option><option value="175">175 - SOUTHAMPTON</option><option value="177">177 - SPOTSYLVANIA</option><option value="179">179 - STAFFORD</option><option value="790">790 - STAUNTON CITY</option><option value="800">800 - SUFFOLK CITY</option><option value="181">181 - SURRY</option><option value="183">183 - SUSSEX</option><option value="185">185 - TAZEWELL</option><option value="810">810 - VIRGINIA BEACH CITY</option><option value="187">187 - WARREN</option><option value="191">191 - WASHINGTON</option><option value="820">820 - WAYNESBORO CITY</option><option value="193">193 - WESTMORELAND</option><option value="830">830 - WILLIAMSBURG CITY</option><option value="840">840 - WINCHESTER CITY</option><option value="195">195 - WISE</option><option value="197">197 - WYTHE</option><option value="199">199 - YORK</option></select>'
fl_counties = '(any county)</option><option value="001">001 - ALACHUA</option><option value="003">003 - BAKER</option><option value="005">005 - BAY</option><option value="007">007 - BRADFORD</option><option value="009">009 - BREVARD</option><option value="011">011 - BROWARD</option><option value="013">013 - CALHOUN</option><option value="015">015 - CHARLOTTE</option><option value="017">017 - CITRUS</option><option value="019">019 - CLAY</option><option value="021">021 - COLLIER</option><option value="023">023 - COLUMBIA</option><option value="027">027 - DE SOTO</option><option value="029">029 - DIXIE</option><option value="031">031 - DUVAL</option><option value="033">033 - ESCAMBIA</option><option value="035">035 - FLAGLER</option><option value="037">037 - FRANKLIN</option><option value="039">039 - GADSDEN</option><option value="041">041 - GILCHRIST</option><option value="043">043 - GLADES</option><option value="045">045 - GULF</option><option value="047">047 - HAMILTON</option><option value="049">049 - HARDEE</option><option value="051">051 - HENDRY</option><option value="053">053 - HERNANDO</option><option value="055">055 - HIGHLANDS</option><option value="057">057 - HILLSBOROUGH</option><option value="059">059 - HOLMES</option><option value="061">061 - INDIAN RIVER</option><option value="063">063 - JACKSON</option><option value="065">065 - JEFFERSON</option><option value="067">067 - LAFAYETTE</option><option value="069">069 - LAKE</option><option value="071">071 - LEE</option><option value="073">073 - LEON</option><option value="075">075 - LEVY</option><option value="077">077 - LIBERTY</option><option value="079">079 - MADISON</option><option value="081">081 - MANATEE</option><option value="083">083 - MARION</option><option value="085">085 - MARTIN</option><option value="086">086 - MIAMI-DADE</option><option value="087">087 - MONROE</option><option value="089">089 - NASSAU</option><option value="091">091 - OKALOOSA</option><option value="093">093 - OKEECHOBEE</option><option value="095">095 - ORANGE</option><option value="097">097 - OSCEOLA</option><option value="099">099 - PALM BEACH</option><option value="101">101 - PASCO</option><option value="103">103 - PINELLAS</option><option value="105">105 - POLK</option><option value="107">107 - PUTNAM</option><option value="109">109 - SAINT JOHNS</option><option value="111">111 - SAINT LUCIE</option><option value="113">113 - SANTA ROSA</option><option value="115">115 - SARASOTA</option><option value="117">117 - SEMINOLE</option><option value="119">119 - SUMTER</option><option value="121">121 - SUWANNEE</option><option value="123">123 - TAYLOR</option><option value="125">125 - UNION</option><option value="127">127 - VOLUSIA</option><option value="129">129 - WAKULLA</option><option value="131">131 - WALTON</option><option value="133">133 - WASHINGTON</option></select>'
tx_counties = '(any county)</option><option value="001">001 - ANDERSON</option><option value="003">003 - ANDREWS</option><option value="005">005 - ANGELINA</option><option value="007">007 - ARANSAS</option><option value="009">009 - ARCHER</option><option value="011">011 - ARMSTRONG</option><option value="013">013 - ATASCOSA</option><option value="015">015 - AUSTIN</option><option value="017">017 - BAILEY</option><option value="019">019 - BANDERA</option><option value="021">021 - BASTROP</option><option value="023">023 - BAYLOR</option><option value="025">025 - BEE</option><option value="027">027 - BELL</option><option value="029">029 - BEXAR</option><option value="031">031 - BLANCO</option><option value="033">033 - BORDEN</option><option value="035">035 - BOSQUE</option><option value="037">037 - BOWIE</option><option value="039">039 - BRAZORIA</option><option value="041">041 - BRAZOS</option><option value="043">043 - BREWSTER</option><option value="045">045 - BRISCOE</option><option value="047">047 - BROOKS</option><option value="049">049 - BROWN</option><option value="051">051 - BURLESON</option><option value="053">053 - BURNET</option><option value="055">055 - CALDWELL</option><option value="057">057 - CALHOUN</option><option value="059">059 - CALLAHAN</option><option value="061">061 - CAMERON</option><option value="063">063 - CAMP</option><option value="065">065 - CARSON</option><option value="067">067 - CASS</option><option value="069">069 - CASTRO</option><option value="071">071 - CHAMBERS</option><option value="073">073 - CHEROKEE</option><option value="075">075 - CHILDRESS</option><option value="077">077 - CLAY</option><option value="079">079 - COCHRAN</option><option value="081">081 - COKE</option><option value="083">083 - COLEMAN</option><option value="085">085 - COLLIN</option><option value="087">087 - COLLINGSWORTH</option><option value="089">089 - COLORADO</option><option value="091">091 - COMAL</option><option value="093">093 - COMANCHE</option><option value="095">095 - CONCHO</option><option value="097">097 - COOKE</option><option value="099">099 - CORYELL</option><option value="101">101 - COTTLE</option><option value="103">103 - CRANE</option><option value="105">105 - CROCKETT</option><option value="107">107 - CROSBY</option><option value="109">109 - CULBERSON</option><option value="111">111 - DALLAM</option><option value="113">113 - DALLAS</option><option value="115">115 - DAWSON</option><option value="123">123 - DE WITT</option><option value="117">117 - DEAF SMITH</option><option value="119">119 - DELTA</option><option value="121">121 - DENTON</option><option value="125">125 - DICKENS</option><option value="127">127 - DIMMIT</option><option value="129">129 - DONLEY</option><option value="131">131 - DUVAL</option><option value="133">133 - EASTLAND</option><option value="135">135 - ECTOR</option><option value="137">137 - EDWARDS</option><option value="141">141 - EL PASO</option><option value="139">139 - ELLIS</option><option value="143">143 - ERATH</option><option value="145">145 - FALLS</option><option value="147">147 - FANNIN</option><option value="149">149 - FAYETTE</option><option value="151">151 - FISHER</option><option value="153">153 - FLOYD</option><option value="155">155 - FOARD</option><option value="157">157 - FORT BEND</option><option value="159">159 - FRANKLIN</option><option value="161">161 - FREESTONE</option><option value="163">163 - FRIO</option><option value="165">165 - GAINES</option><option value="167">167 - GALVESTON</option><option value="169">169 - GARZA</option><option value="171">171 - GILLESPIE</option><option value="173">173 - GLASSCOCK</option><option value="175">175 - GOLIAD</option><option value="177">177 - GONZALES</option><option value="179">179 - GRAY</option><option value="181">181 - GRAYSON</option><option value="183">183 - GREGG</option><option value="185">185 - GRIMES</option><option value="187">187 - GUADALUPE</option><option value="189">189 - HALE</option><option value="191">191 - HALL</option><option value="193">193 - HAMILTON</option><option value="195">195 - HANSFORD</option><option value="197">197 - HARDEMAN</option><option value="199">199 - HARDIN</option><option value="201">201 - HARRIS</option><option value="203">203 - HARRISON</option><option value="205">205 - HARTLEY</option><option value="207">207 - HASKELL</option><option value="209">209 - HAYS</option><option value="211">211 - HEMPHILL</option><option value="213">213 - HENDERSON</option><option value="215">215 - HIDALGO</option><option value="217">217 - HILL</option><option value="219">219 - HOCKLEY</option><option value="221">221 - HOOD</option><option value="223">223 - HOPKINS</option><option value="225">225 - HOUSTON</option><option value="227">227 - HOWARD</option><option value="229">229 - HUDSPETH</option><option value="231">231 - HUNT</option><option value="233">233 - HUTCHINSON</option><option value="235">235 - IRION</option><option value="237">237 - JACK</option><option value="239">239 - JACKSON</option><option value="241">241 - JASPER</option><option value="243">243 - JEFF DAVIS</option><option value="245">245 - JEFFERSON</option><option value="247">247 - JIM HOGG</option><option value="249">249 - JIM WELLS</option><option value="251">251 - JOHNSON</option><option value="253">253 - JONES</option><option value="255">255 - KARNES</option><option value="257">257 - KAUFMAN</option><option value="259">259 - KENDALL</option><option value="261">261 - KENEDY</option><option value="263">263 - KENT</option><option value="265">265 - KERR</option><option value="267">267 - KIMBLE</option><option value="269">269 - KING</option><option value="271">271 - KINNEY</option><option value="273">273 - KLEBERG</option><option value="275">275 - KNOX</option><option value="283">283 - LA SALLE</option><option value="277">277 - LAMAR</option><option value="279">279 - LAMB</option><option value="281">281 - LAMPASAS</option><option value="285">285 - LAVACA</option><option value="287">287 - LEE</option><option value="289">289 - LEON</option><option value="291">291 - LIBERTY</option><option value="293">293 - LIMESTONE</option><option value="295">295 - LIPSCOMB</option><option value="297">297 - LIVE OAK</option><option value="299">299 - LLANO</option><option value="301">301 - LOVING</option><option value="303">303 - LUBBOCK</option><option value="305">305 - LYNN</option><option value="313">313 - MADISON</option><option value="315">315 - MARION</option><option value="317">317 - MARTIN</option><option value="319">319 - MASON</option><option value="321">321 - MATAGORDA</option><option value="323">323 - MAVERICK</option><option value="307">307 - MCCULLOCH</option><option value="309">309 - MCLENNAN</option><option value="311">311 - MCMULLEN</option><option value="325">325 - MEDINA</option><option value="327">327 - MENARD</option><option value="329">329 - MIDLAND</option><option value="331">331 - MILAM</option><option value="333">333 - MILLS</option><option value="335">335 - MITCHELL</option><option value="337">337 - MONTAGUE</option><option value="339">339 - MONTGOMERY</option><option value="341">341 - MOORE</option><option value="343">343 - MORRIS</option><option value="345">345 - MOTLEY</option><option value="347">347 - NACOGDOCHES</option><option value="349">349 - NAVARRO</option><option value="351">351 - NEWTON</option><option value="353">353 - NOLAN</option><option value="355">355 - NUECES</option><option value="357">357 - OCHILTREE</option><option value="359">359 - OLDHAM</option><option value="361">361 - ORANGE</option><option value="363">363 - PALO PINTO</option><option value="365">365 - PANOLA</option><option value="367">367 - PARKER</option><option value="369">369 - PARMER</option><option value="371">371 - PECOS</option><option value="373">373 - POLK</option><option value="375">375 - POTTER</option><option value="377">377 - PRESIDIO</option><option value="379">379 - RAINS</option><option value="381">381 - RANDALL</option><option value="383">383 - REAGAN</option><option value="385">385 - REAL</option><option value="387">387 - RED RIVER</option><option value="389">389 - REEVES</option><option value="391">391 - REFUGIO</option><option value="393">393 - ROBERTS</option><option value="395">395 - ROBERTSON</option><option value="397">397 - ROCKWALL</option><option value="399">399 - RUNNELS</option><option value="401">401 - RUSK</option><option value="403">403 - SABINE</option><option value="405">405 - SAN AUGUSTINE</option><option value="407">407 - SAN JACINTO</option><option value="409">409 - SAN PATRICIO</option><option value="411">411 - SAN SABA</option><option value="413">413 - SCHLEICHER</option><option value="415">415 - SCURRY</option><option value="417">417 - SHACKELFORD</option><option value="419">419 - SHELBY</option><option value="421">421 - SHERMAN</option><option value="423">423 - SMITH</option><option value="425">425 - SOMERVELL</option><option value="427">427 - STARR</option><option value="429">429 - STEPHENS</option><option value="431">431 - STERLING</option><option value="433">433 - STONEWALL</option><option value="435">435 - SUTTON</option><option value="437">437 - SWISHER</option><option value="439">439 - TARRANT</option><option value="441">441 - TAYLOR</option><option value="443">443 - TERRELL</option><option value="445">445 - TERRY</option><option value="447">447 - THROCKMORTON</option><option value="449">449 - TITUS</option><option value="451">451 - TOM GREEN</option><option value="453">453 - TRAVIS</option><option value="455">455 - TRINITY</option><option value="457">457 - TYLER</option><option value="459">459 - UPSHUR</option><option value="461">461 - UPTON</option><option value="463">463 - UVALDE</option><option value="465">465 - VAL VERDE</option><option value="467">467 - VAN ZANDT</option><option value="469">469 - VICTORIA</option><option value="471">471 - WALKER</option><option value="473">473 - WALLER</option><option value="475">475 - WARD</option><option value="477">477 - WASHINGTON</option><option value="479">479 - WEBB</option><option value="481">481 - WHARTON</option><option value="483">483 - WHEELER</option><option value="485">485 - WICHITA</option><option value="487">487 - WILBARGER</option><option value="489">489 - WILLACY</option><option value="491">491 - WILLIAMSON</option><option value="493">493 - WILSON</option><option value="495">495 - WINKLER</option><option value="497">497 - WISE</option><option value="499">499 - WOOD</option><option value="501">501 - YOAKUM</option><option value="503">503 - YOUNG</option><option value="505">505 - ZAPATA</option><option value="507">507 - ZAVALA</option></select>'

svc_states = {"CA":ca_counties, "VA": va_counties, "FL":fl_counties, "TX":tx_counties}



def get_all_states():
    for state in us_states:
        for area in areas:
            print("downloading : " , state[0], ", ", area)
            get_state_data(state[1], area)

def get_counties(raw_counties):
    return re.findall(r'value="(\d+)"', raw_counties)



def get_big_svc_states():
    for state in svc_states:
        counties =  get_counties(svc_states[state])
        for c in counties:
            print("getting : ",state, ", ", c )
            get_state_data(state, "SVC", c )



def scrape_pages():
    get_all_states()
    get_big_svc_states()



