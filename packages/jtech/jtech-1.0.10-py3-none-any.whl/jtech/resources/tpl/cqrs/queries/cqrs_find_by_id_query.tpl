/*
*  @(#)Find{{ className }}ByIdQuery.java
*
*  Copyright (c) J-Tech Solucoes em Informatica.
*  All Rights Reserved.
*
*  This software is the confidential and proprietary information of J-Tech.
*  ("Confidential Information"). You shall not disclose such Confidential
*  Information and shall use it only in accordance with the terms of the
*  license agreement you entered into with J-Tech.
*
*/
package {{ package }}.services.queries.query;

{% if isJpa %}import java.util.UUID;{% endif %}

/**
* class Find{{ className }}ByIdQuery
*
* @author {{ username }}
*/
public record Find{{ className }}ByIdQuery({% if isMongo and not isJpa %}String{% elif isJpa %}UUID{% else %}String{% endif %} id) {
}
