/* Construction of the table france_rues from france */
SELECT voie,code_post,nom_comm
INTO france_rues
FROM france
GROUP BY voie,code_post,nom_comm
ORDER BY nom_comm;