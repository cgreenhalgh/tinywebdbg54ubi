/**
 * Copyright 2010 The University of Nottingham
 * 
 * This file is part of tinywebdbg54ubi.
 *
 *  tinywebdbg54ubi is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  tinywebdbg54ubi is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with tinywebdbg54ubi.  If not, see <http://www.gnu.org/licenses/>.
 * 
 */
package uk.ac.nott.cs.g54ubi.tinywebdb;

import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.KeyFactory;

import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.IdGeneratorStrategy;
import javax.jdo.annotations.PrimaryKey;

import java.util.Date;

/** Persistent value (!)
 * @author cmg
 *
 */
@PersistenceCapable
public class PersistentValue {
	/** app engine store id - user / tag */
    @PrimaryKey
    @Persistent(valueStrategy = IdGeneratorStrategy.IDENTITY)
    private Key key;
    /** user id */
    @Persistent
	private String user;
    /** tag */
    @Persistent
	private String tag;
    /** value string */
    @Persistent
	private String value;
    /** data value created */
    @Persistent
    private Date created;
	/**
	 * 
	 */
	public PersistentValue() {
		super();
		created = new Date();
	}
    /** map user / tag to key */
	public static Key getKey(String user, String tag) {
		String digest = HashFactory.getDigest(user)+"-"+HashFactory.getDigest(tag);
		Key key = KeyFactory.createKey(PersistentValue.class.getSimpleName(), digest);
		return key;
	}
	/**
	 * @param user
	 * @param tag
	 * @param value
	 */
	public PersistentValue(String user, String tag, String value) {
		super();
		this.user = user;
		this.tag = tag;
		this.value = value;
		created = new Date();
		key = getKey(user, tag);
	}
	/**
	 * @return the key
	 */
	public Key getKey() {
		return key;
	}
	/**
	 * @param key the key to set
	 */
	public void setKey(Key key) {
		this.key = key;
	}
	/**
	 * @return the user
	 */
	public String getUser() {
		return user;
	}
	/**
	 * @param user the user to set
	 */
	public void setUser(String user) {
		this.user = user;
	}
	/**
	 * @return the tag
	 */
	public String getTag() {
		return tag;
	}
	/**
	 * @param tag the tag to set
	 */
	public void setTag(String tag) {
		this.tag = tag;
	}
	/**
	 * @return the value
	 */
	public String getValue() {
		return value;
	}
	/**
	 * @param value the value to set
	 */
	public void setValue(String value) {
		this.value = value;
	}
	/**
	 * @return the created
	 */
	public Date getCreated() {
		return created;
	}
	/**
	 * @param created the created to set
	 */
	public void setCreated(Date created) {
		this.created = created;
	}
	
}
