# rss_tests.py  (c)2019  Henrique Moreira

"""
  rss_tests: tests for rsread.py module, etc.

  Compatibility: python 3.
"""

from rsread import *
from redito import xCharMap


#
# main_rss_tests()
#
def main_rss_tests (outFile, errFile, inArgs):
    code = None
    debug = 0
    verbose = 0
    rs = RssEcho()
    s = rss_sample()
    s = xCharMap.simpler_ascii( s )
    rs.add_from_string( s )
    n = len( rs.content )
    if debug>0:
        errFile.write("Lines: {}\n".format( n ))
        i = 0
        for a in rs.content:
            print("Line {}: {}".format( rs.originalInput[ i ], a ))
            i += 1
    sCont = "\n".join( rs.content ).encode( "ascii" )
    y = etree.fromstring( sCont )
    print(">>>")
    for e in y.iter():
        print("tag: {},\n'{}'\n".format(e.tag, e.text))
    print("<<<")
    return code


#
# RSS sample
#
def rss_sample (i=0):
    aText = """
<!-- downloaded from http://www.rtp.pt/play/podcast/260 , 21.10.2019 -->
<?xml version="1.0" encoding="utf-8"?>
 <rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0" xml:lang="pt-PT" >
	 <channel>
	  <title>Prova Oral</title>
	  <link>https://www.rtp.pt/play/p260/prova-oral</link>
	  <description>O programa mais interativo da rádio, com temas diferentes, convidados diferentes e muita animação.</description>
	  <itunes:author>RTP - Rádio e Televisão de Portugal - Antena3</itunes:author>
	  <itunes:summary>O programa mais interativo da rádio, com temas diferentes, convidados diferentes e muita animação.</itunes:summary>
	  <itunes:explicit>no</itunes:explicit>
	  <itunes:keywords>RTP, RTP - Rádio e Televisão de Portugal - Antena3, Fórum, Prova Oral</itunes:keywords>
	  <language>pt</language>
	  <copyright>© RTP</copyright>
	  <webMaster>podcasts@rtp.pt</webMaster>
	  <itunes:owner>
	  <itunes:name></itunes:name>
    <itunes:copyright>968555</itunes:copyright>
	  <itunes:email>podcasts@rtp.pt</itunes:email>
	  </itunes:owner>
	  <itunes:block>no</itunes:block>
	  <itunes:category text="Society &amp; Culture"></itunes:category>
	  <itunes:image href="http://img0.rtp.pt/EPG/radio/imagens/PO1070_417_75391.jpg" />
	  <image>
		<url>http://img0.rtp.pt/EPG/radio/imagens/PO1070_417_75391.jpg</url>
		<title>Prova Oral</title>
		<link>https://www.rtp.pt/play/p260/prova-oral</link>
		<width>160</width>
		<height>120</height>
	  </image>
	  <lastBuildDate>Mon, 21 Oct 2019 7:08:22 +0100</lastBuildDate>
	<item>
	    <title> Festival Idiota 2019 </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Fri, 18 Oct 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1910/6062173_310069-1910211746.mp3" length="57267200" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1910/6062173_310069-1910211746.mp3</guid>
	    <itunes:duration>00:58:15</itunes:duration>
	</item>	<item>
	    <title> Joana Sá e Henrique Paranhos falam sobre trabalho remoto </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Thu, 17 Oct 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1910/6057375_309771-1910172013.mp3" length="56297472" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1910/6057375_309771-1910172013.mp3</guid>
	    <itunes:duration>00:57:16</itunes:duration>
	</item>	<item>
	    <title> Joana Sá e Henrique Paranhos falam sobre trabalho remoto </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Thu, 17 Oct 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1910/6057375_309771-1910172013.mp3" length="56297472" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1910/6057375_309771-1910172013.mp3</guid>
	    <itunes:duration>00:57:16</itunes:duration>
	</item>	<item>
	    <title> Rui Pereira, Sónia Seixas e Tito de Morais falam sobre Cyberbullying </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Wed, 16 Oct 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1910/6055088_309625-1910162009.mp3" length="55334912" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1910/6055088_309625-1910162009.mp3</guid>
	    <itunes:duration>00:56:17</itunes:duration>
	</item>	<item>
	    <title> Soraia Simões de Andrade com Fixar o (In)visível </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Tue, 15 Oct 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1910/6052990_309502-1910152043.mp3" length="53512192" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1910/6052990_309502-1910152043.mp3</guid>
	    <itunes:duration>00:54:26</itunes:duration>
	</item>	<item>
	    <title> Rui Marques e &quot;A Pitada do Pai&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Mon, 14 Oct 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1910/6052547_309471-1910151648.mp3" length="54605824" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1910/6052547_309471-1910151648.mp3</guid>
	    <itunes:duration>00:55:32</itunes:duration>
	</item>	<item>
	    <title> Leandro Morgado fala sobre Mentalismo </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Fri, 11 Oct 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1910/6047856_309243-1910112013.mp3" length="58390528" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1910/6047856_309243-1910112013.mp3</guid>
	    <itunes:duration>00:59:23</itunes:duration>
	</item>	<item>
	    <title> Ao vivo do FOLIO (Festival Literário Internacional de Óbidos) </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Thu, 10 Oct 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1910/6045162_309062-1910101742.mp3" length="51897344" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1910/6045162_309062-1910101742.mp3</guid>
	    <itunes:duration>00:52:47</itunes:duration>
	</item>	<item>
	    <title> Diogo Patrocínio, Lazlo Varga e João Garcia falam sobre o Festival Banff </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Wed, 09 Oct 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1910/6042857_308955-1910092011.mp3" length="54475776" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1910/6042857_308955-1910092011.mp3</guid>
	    <itunes:duration>00:55:24</itunes:duration>
	</item>	<item>
	    <title> Maria Elisa com 40 anos do SNS </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Tue, 08 Oct 2019 12:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1910/6040847_308840-1910082100.mp3" length="56847360" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1910/6040847_308840-1910082100.mp3</guid>
	    <itunes:duration>00:57:49</itunes:duration>
	</item>	<item>
	    <title> Luís Osório, Miguel Fragata e Tiago Rodrigues falam sobre Fake News </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Mon, 07 Oct 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1910/6038630_308698-1910072015.mp3" length="56531968" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1910/6038630_308698-1910072015.mp3</guid>
	    <itunes:duration>00:57:30</itunes:duration>
	</item>	<item>
	    <title> Daniel Carapeto com &quot;Tragédia&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Fri, 04 Oct 2019 12:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1910/6035911_308537-1910042013.mp3" length="55826432" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1910/6035911_308537-1910042013.mp3</guid>
	    <itunes:duration>00:56:47</itunes:duration>
	</item>	<item>
	    <title> Ruben Obadia sobre &quot;Fuckup Nights&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Thu, 03 Oct 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1910/6033719_308334-1910032010.mp3" length="52383744" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1910/6033719_308334-1910032010.mp3</guid>
	    <itunes:duration>00:53:17</itunes:duration>
	</item>	<item>
	    <title> Miguel Coutinho, Inês Grosso e Paulo Furtado falam do aniversário do MAAT </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Wed, 02 Oct 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1910/6031032_308213-1910022014.mp3" length="54860800" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1910/6031032_308213-1910022014.mp3</guid>
	    <itunes:duration>00:55:48</itunes:duration>
	</item>	<item>
	    <title> Ao vivo no Congresso dos Cozinheiros </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Tue, 01 Oct 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1910/6028390_308062-1910011642.mp3" length="53780480" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1910/6028390_308062-1910011642.mp3</guid>
	    <itunes:duration>00:54:42</itunes:duration>
	</item>	<item>
	    <title> Falamos do Bairro Metropolitan com Gonçalo Morais Leitão </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Mon, 30 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/6026713_307969-1909302014.mp3" length="54992896" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/6026713_307969-1909302014.mp3</guid>
	    <itunes:duration>00:55:56</itunes:duration>
	</item>	<item>
	    <title> Samuel Úria e Hugo Sousa </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Fri, 27 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/6023896_307813-1909272042.mp3" length="54679552" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/6023896_307813-1909272042.mp3</guid>
	    <itunes:duration>00:55:37</itunes:duration>
	</item>	<item>
	    <title> Sandra Duarte Tavares com &quot;Comunicar com Sucesso&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Thu, 26 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/6021990_307654-1909262015.mp3" length="56683520" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/6021990_307654-1909262015.mp3</guid>
	    <itunes:duration>00:57:39</itunes:duration>
	</item>	<item>
	    <title> João Graça, Maria Antunes e Rui Catalão sobre o Couraveg </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Wed, 25 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/6019906_307521-1909252014.mp3" length="55478272" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/6019906_307521-1909252014.mp3</guid>
	    <itunes:duration>00:56:26</itunes:duration>
	</item>	<item>
	    <title> Rui Zink com &quot;O Manual do Bom Fascista&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Tue, 24 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/6017878_307390-1909242013.mp3" length="57997312" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/6017878_307390-1909242013.mp3</guid>
	    <itunes:duration>00:58:59</itunes:duration>
	</item>	<item>
	    <title> Filipa Marinho, Catarina Monteiro e Mariana Duarte Silva com She Said So </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Mon, 23 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/6015152_307257-1909232013.mp3" length="57001984" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/6015152_307257-1909232013.mp3</guid>
	    <itunes:duration>00:57:59</itunes:duration>
	</item>	<item>
	    <title> José Luís Peixoto com &quot;Autobiografia&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Fri, 20 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/6011759_307115-1909202034.mp3" length="54622208" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/6011759_307115-1909202034.mp3</guid>
	    <itunes:duration>00:55:33</itunes:duration>
	</item>	<item>
	    <title> Afonso Reis Cabral e Caio. </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Thu, 19 Sep 2019 12:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/6009982_306982-1909192355.mp3" length="56380416" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/6009982_306982-1909192355.mp3</guid>
	    <itunes:duration>00:57:21</itunes:duration>
	</item>	<item>
	    <title> Marco Neves com Gramática para todos </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Wed, 18 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/6007836_306833-1909182012.mp3" length="55554048" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/6007836_306833-1909182012.mp3</guid>
	    <itunes:duration>00:56:30</itunes:duration>
	</item>	<item>
	    <title> Rita Silva Freire com &quot;Trazer ao Mundo&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Tue, 17 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/6007728_306830-1909181922.mp3" length="54719488" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/6007728_306830-1909181922.mp3</guid>
	    <itunes:duration>00:55:39</itunes:duration>
	</item>	<item>
	    <title> Surf Out Portugal com Tiago Pires e Patrick Stilwell </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Mon, 16 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/6004953_306670-1909171405.mp3" length="55723008" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/6004953_306670-1909171405.mp3</guid>
	    <itunes:duration>00:56:41</itunes:duration>
	</item>	<item>
	    <title> Falamos de sonhos com Sidarta Ribeiro </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Fri, 13 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/6005677_306711-1909171926.mp3" length="54644736" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/6005677_306711-1909171926.mp3</guid>
	    <itunes:duration>00:55:35</itunes:duration>
	</item>	<item>
	    <title> Emissão ao vivo na Comic Con </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Thu, 12 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/5999385_306309-1909121754.mp3" length="56115200" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/5999385_306309-1909121754.mp3</guid>
	    <itunes:duration>00:57:04</itunes:duration>
	</item>	<item>
	    <title> Falamos sobre Sustentabilidade com Rute Caldeira, Filipa Maló, Eunice Maya e Joana Limão </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Wed, 11 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/5997693_306212-1909112016.mp3" length="56212480" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/5997693_306212-1909112016.mp3</guid>
	    <itunes:duration>00:57:10</itunes:duration>
	</item>	<item>
	    <title> Falamos sobre o Festival Andamento da RTP </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Tue, 10 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/5995844_306101-1909102013.mp3" length="55021568" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/5995844_306101-1909102013.mp3</guid>
	    <itunes:duration>00:55:58</itunes:duration>
	</item>	<item>
	    <title> Leonídio Paulo Ferreira com Encontros e encontrões de Portugal no Mundo </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Mon, 09 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/5994047_305974-1909092013.mp3" length="55161856" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/5994047_305974-1909092013.mp3</guid>
	    <itunes:duration>00:56:06</itunes:duration>
	</item>	<item>
	    <title> Pipoca Mais Doce e Agora Deu-me Para Isto </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Fri, 06 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/5993740_305960-1909091619.mp3" length="54890496" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/5993740_305960-1909091619.mp3</guid>
	    <itunes:duration>00:55:50</itunes:duration>
	</item>	<item>
	    <title> Miguel Ribeiro com &quot;Beyond Darwin: The Program Hypothesis&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Thu, 05 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/5989704_305735-1909052021.mp3" length="54820864" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/5989704_305735-1909052021.mp3</guid>
	    <itunes:duration>00:55:45</itunes:duration>
	</item>	<item>
	    <title> Mr. António McFlirty e Ms. Lolita VonTease falam sobre o Tinder </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Wed, 04 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/5987334_305653-1909042014.mp3" length="56905728" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/5987334_305653-1909042014.mp3</guid>
	    <itunes:duration>00:57:53</itunes:duration>
	</item>	<item>
	    <title> Falamos com o actor Miguel Loureiro </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Tue, 03 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/5985039_305558-1909032013.mp3" length="56011776" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/5985039_305558-1909032013.mp3</guid>
	    <itunes:duration>00:56:58</itunes:duration>
	</item>	<item>
	    <title> Beatriz Gosta com &quot;Quem Acredita Vai&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Mon, 02 Sep 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1909/5983247_305501-1909022010.mp3" length="55951360" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1909/5983247_305501-1909022010.mp3</guid>
	    <itunes:duration>00:56:55</itunes:duration>
	</item>	<item>
	    <title> Tema Livre antes das férias </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Thu, 01 Aug 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1908/5948012_303705-1908012014.mp3" length="54561792" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1908/5948012_303705-1908012014.mp3</guid>
	    <itunes:duration>00:55:30</itunes:duration>
	</item>	<item>
	    <title> Filipa Range com o Desafio Vegan </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Wed, 31 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5946241_303616-1907312012.mp3" length="54914048" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5946241_303616-1907312012.mp3</guid>
	    <itunes:duration>00:55:51</itunes:duration>
	</item>	<item>
	    <title> Marta Durán e as &quot;Boleias da Marta&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Tue, 30 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5944433_303531-1907302014.mp3" length="54872064" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5944433_303531-1907302014.mp3</guid>
	    <itunes:duration>00:55:49</itunes:duration>
	</item>	<item>
	    <title> O Youtube segundo Sir Kazzio </title>
	    <itunes:subtitle/>
	    <itunes:summary>O programa mais interativo da Rádio, com temas diferentes, convidados diferentes e muita animação.</itunes:summary>

	    <description>O programa mais interativo da Rádio, com temas diferentes, convidados diferentes e muita animação.</description>
	    <pubDate>Mon, 29 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5942996_303432-1907292015.mp3" length="55809024" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5942996_303432-1907292015.mp3</guid>
	    <itunes:duration>00:56:46</itunes:duration>
	</item>	<item>
	    <title> Andreia Vale com &quot;Da Boca Para Fora&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Fri, 26 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5940900_303334-1907262016.mp3" length="56426496" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5940900_303334-1907262016.mp3</guid>
	    <itunes:duration>00:57:23</itunes:duration>
	</item>	<item>
	    <title> Chef Paco Roncero </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Thu, 25 Jul 2019 12:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5938878_303224-1907252225.mp3" length="50418688" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5938878_303224-1907252225.mp3</guid>
	    <itunes:duration>00:51:17</itunes:duration>
	</item>	<item>
	    <title> Marco Paulo </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Wed, 24 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5940803_303328-1907261936.mp3" length="57358336" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5940803_303328-1907261936.mp3</guid>
	    <itunes:duration>00:58:20</itunes:duration>
	</item>	<item>
	    <title> Aurora Pinho </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Tue, 23 Jul 2019 12:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5935119_302997-1907232055.mp3" length="56428544" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5935119_302997-1907232055.mp3</guid>
	    <itunes:duration>00:57:24</itunes:duration>
	</item>	<item>
	    <title> Ana Moniz e &quot;Este Livro Não É Para Fracos&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Mon, 22 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5933191_302909-1907222015.mp3" length="53828608" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5933191_302909-1907222015.mp3</guid>
	    <itunes:duration>00:54:45</itunes:duration>
	</item>	<item>
	    <title> Fátima Mariano e os
&quot;Grandes Mistérios da História de Portugal&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Fri, 19 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5930436_302788-1907192019.mp3" length="53342208" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5930436_302788-1907192019.mp3</guid>
	    <itunes:duration>00:54:15</itunes:duration>
	</item>	<item>
	    <title> José Castelo Branco </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Wed, 17 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5927004_302486-1907172018.mp3" length="59120640" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5927004_302486-1907172018.mp3</guid>
	    <itunes:duration>01:00:08</itunes:duration>
	</item>	<item>
	    <title> Entrevista a Elza Soares </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Tue, 16 Jul 2019 8:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5925037_302378-1907161920.mp3" length="53228544" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5925037_302378-1907161920.mp3</guid>
	    <itunes:duration>00:54:08</itunes:duration>
	</item>	<item>
	    <title> Tema Livre </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Mon, 15 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5923457_302243-1907152012.mp3" length="55649280" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5923457_302243-1907152012.mp3</guid>
	    <itunes:duration>00:56:36</itunes:duration>
	</item>	<item>
	    <title> Maria Gonçalves com &quot;Influencia&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Fri, 12 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5920841_302039-1907122016.mp3" length="54672384" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5920841_302039-1907122016.mp3</guid>
	    <itunes:duration>00:55:36</itunes:duration>
	</item>	<item>
	    <title> Rudolf Gruner, Isabel Marques e Pedro Castro falam sobre o Observador </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Thu, 11 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5919267_301897-1907112016.mp3" length="54599680" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5919267_301897-1907112016.mp3</guid>
	    <itunes:duration>00:55:32</itunes:duration>
	</item>	<item>
	    <title> Ângelo Valente, Sofia Nunes e Maria Inês Santos com &quot;Antes de morrer quero&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Wed, 10 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5917457_301750-1907102011.mp3" length="55816192" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5917457_301750-1907102011.mp3</guid>
	    <itunes:duration>00:56:46</itunes:duration>
	</item>	<item>
	    <title> João Carlos Melo fala sobre auto estima </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Tue, 09 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5915483_301628-1907092010.mp3" length="54642688" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5915483_301628-1907092010.mp3</guid>
	    <itunes:duration>00:55:35</itunes:duration>
	</item>	<item>
	    <title> Anabela Mota Ribeiro, André Teodósio, Miguel Bica e Tiago Sigorelho falam sobre Cultura </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Mon, 08 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5913789_301499-1907082010.mp3" length="56151040" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5913789_301499-1907082010.mp3</guid>
	    <itunes:duration>00:57:07</itunes:duration>
	</item>	<item>
	    <title> Michael Cunningham  </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Fri, 05 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5910716_301277-1907051506.mp3" length="56776704" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5910716_301277-1907051506.mp3</guid>
	    <itunes:duration>00:57:45</itunes:duration>
	</item>	<item>
	    <title> Maratona de Leitura da Sertã </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Thu, 04 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5909296_301177-1907042009.mp3" length="57556992" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5909296_301177-1907042009.mp3</guid>
	    <itunes:duration>00:58:32</itunes:duration>
	</item>	<item>
	    <title> Hélio Morais, Tiago Santos Paiva e Catarina Matos falam sobre o NOS Alive </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Wed, 03 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5906914_301026-1907032017.mp3" length="57362432" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5906914_301026-1907032017.mp3</guid>
	    <itunes:duration>00:58:21</itunes:duration>
	</item>	<item>
	    <title> Mami Pereira e as &quot;Crónicas Mami Geographic&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Tue, 02 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5904921_300928-1907022013.mp3" length="57088000" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5904921_300928-1907022013.mp3</guid>
	    <itunes:duration>00:58:04</itunes:duration>
	</item>	<item>
	    <title> Pierre Aderne com a &quot;Rua das Pretas&quot; </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Mon, 01 Jul 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1907/5903157_300808-1907012006.mp3" length="54497280" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1907/5903157_300808-1907012006.mp3</guid>
	    <itunes:duration>00:55:26</itunes:duration>
	</item>	<item>
	    <title> Ao vivo do Kids Music Fest </title>
	    <itunes:subtitle/>
	    <itunes:summary></itunes:summary>

	    <description></description>
	    <pubDate>Fri, 28 Jun 2019 7:00:00 +0100</pubDate>
	    <enclosure url="http://podcasts.rtp.pt/nas2.share/wavrss/at3/1906/5900132_300614-1906281640.mp3" length="54465536" type="audio/mpeg"/>
	    <guid isPermaLink="true" >http://cdn-ondemand.rtp.pt/podcasts/at3/1906/5900132_300614-1906281640.mp3</guid>
	    <itunes:duration>00:55:24</itunes:duration>
	</item></channel>
</rss>
"""
    return aText


#
# Main script
#
if __name__ == "__main__":
    import sys
    code = main_rss_tests( sys.stdout, sys.stderr, sys.argv[ 1: ] )
    if code is None:
        print("""rss_tests
""")
        code = 0
    assert type( code )==int
    assert code<=127
    sys.exit( code )
