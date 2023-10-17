#ifndef XMLTOJSON_HPP_INCLUDED
#define XMLTOJSON_HPP_INCLUDED

#include <iostream>
#include <map>
#include <string>
#include <cctype>
#include <cstring>
#include <exception>

#include "rapidxml/rapidxml.hpp"
#include "rapidxml/rapidxml_utils.hpp"
#include "rapidxml/rapidxml_print.hpp"

#include "rapidjson/document.h"
#include "rapidjson/prettywriter.h"
#include "rapidjson/encodedstream.h"
#include "rapidjson/stringbuffer.h"
#include "rapidjson/reader.h"
#include "rapidjson/writer.h"
#include "rapidjson/filereadstream.h"
#include "rapidjson/filewritestream.h"
#include "rapidjson/error/en.h"

/* [Start] This part is configurable */
static const char xmltojson_text_additional_name[] = "#text";
static const char xmltojson_attribute_name_prefix[] = "@";
/* Example:
   <node_name attribute_name="attribute_value">value</node_name> ---> "node_name":{"#text":"value","@attribute_name":"attribute_value"}
*/
static const bool xmltojson_numeric_support = false;
/* Example:
   xmltojson_numeric_support = false:
   <number>26.026</number>  ---> "number":"26.026"
   xmltojson_numeric_support = true:
   <number>26.026</number>  ---> "number":26.026
*/
/* [End]   This part is configurable */

class xmltojson_parse_error: public std::runtime_error
{
public:
    xmltojson_parse_error(const char *what, const std::exception& e)
        : std::runtime_error(what)
    {
        m_message = std::string(this->what());
        m_details = std::string(e.what());
    }

    xmltojson_parse_error(const char *what)
        : std::runtime_error(what)
    {
    }

    std::string GetString() {
        return "Exception: " + m_message + ", Details: " + m_details;
    }

private:
    std::string m_message;
    std::string m_details;
};

// Avoided any namespace pollution.
static bool xmltojson_has_digits_only(const char *input, bool *hasDecimal)
{
    if (input == nullptr)
        return false;  // treat empty input as a string (probably will be an empty string)

    const char * runPtr = input;

    *hasDecimal = false;

    while (*runPtr != '\0')
    {
        if (*runPtr == '.')
        {
            if (!(*hasDecimal))
                *hasDecimal = true;
            else
                return false; // we found two dots - not a number
        }
        else if (isalpha(*runPtr))
        {
            return false;
        }
        runPtr++;
    }

    return true;
}

void xmltojson_to_array_form(const char *name, rapidjson::Value &jsvalue, rapidjson::Value &jsvalue_chd, rapidjson::Document::AllocatorType& allocator)
{
    rapidjson::Value jsvalue_target; // target to do some operation
    rapidjson::Value jn;             // this is a must, partially because of the latest version of rapidjson
    jn.SetString(name, allocator);
    jsvalue_target = jsvalue.FindMember(name)->value;
    if(jsvalue_target.IsArray())
    {
        jsvalue_target.PushBack(jsvalue_chd, allocator);
        jsvalue.RemoveMember(name);
        jsvalue.AddMember(jn, jsvalue_target, allocator);
    }
    else
    {
        rapidjson::Value jsvalue_array;
        //jsvalue_array = jsvalue_target;
        jsvalue_array.SetArray();
        jsvalue_array.PushBack(jsvalue_target, allocator);
        jsvalue_array.PushBack(jsvalue_chd, allocator);
        jsvalue.RemoveMember(name);
        jsvalue.AddMember(jn, jsvalue_array, allocator);
    }
}

void xmltojson_add_attributes(rapidxml::xml_node<> *xmlnode, rapidjson::Value &jsvalue, rapidjson::Document::AllocatorType& allocator)
{
    rapidxml::xml_attribute<> *myattr;
    for(myattr = xmlnode->first_attribute(); myattr; myattr = myattr->next_attribute())
    {
        rapidjson::Value jn, jv;
        jn.SetString((std::string(xmltojson_attribute_name_prefix) + myattr->name()).c_str(), allocator);

        if (xmltojson_numeric_support == false)
        {
            jv.SetString(myattr->value(), allocator);
        }
        else
        {
            bool hasDecimal;
            if (xmltojson_has_digits_only(myattr->value(), &hasDecimal) == false)
            {
                jv.SetString(myattr->value(), allocator);
            }
            else
            {
                if (hasDecimal)
                {
                    double value = std::strtod(myattr->value(),nullptr);
                    jv.SetDouble(value);
                }
                else
                {
                    long int value = std::strtol(myattr->value(), nullptr, 0);
                    jv.SetInt(value);
                }
            }
        }
        jsvalue.AddMember(jn, jv, allocator);
    }
}

void xmltojson_add_ns_prefix(rapidxml::xml_node<> *xmlnode) {
    char *xmlnode_prefix = xmlnode->prefix();
    if (xmlnode_prefix == nullptr) return;

    char *xmlnode_name = xmlnode->name();
    char *xmlnode_name_with_prefix = new char[strlen(xmlnode_prefix) + strlen(xmlnode_name) + 1];

    strcpy(xmlnode_name_with_prefix, xmlnode_prefix);
    strcat(xmlnode_name_with_prefix, ":");
    strcat(xmlnode_name_with_prefix, xmlnode_name);

    xmlnode->name(xmlnode_name_with_prefix);
}

void xmltojson_strip_text(rapidxml::xml_node<> *xmlnode) {
    char* xmlnode_start = xmlnode->value();
    char* xmlnode_end = xmlnode_start;

    while (*xmlnode_start) {
        if (!std::isspace(static_cast<unsigned char>(*xmlnode_start))) {
            *xmlnode_end = *xmlnode_start;
            xmlnode_end++;
        }
        xmlnode_start++;
    }

    *xmlnode_end = '\0';
}

void xmltojson_traverse_node(rapidxml::xml_node<> *xmlnode, rapidjson::Value &jsvalue, rapidjson::Document::AllocatorType& allocator)
{
    // std::cout << "this: " << xmlnode->type() << " name: " << xmlnode->name() << " value: " << xmlnode->value() << '\n';
    rapidjson::Value jsvalue_chd;

    jsvalue.SetObject();
    jsvalue_chd.SetObject();
    rapidxml::xml_node<> *xmlnode_chd;

    // classified discussion:
    if((xmlnode->type() == rapidxml::node_data || xmlnode->type() == rapidxml::node_cdata) && xmlnode->value())
    {
        // case: pure_text
        jsvalue.SetString(xmlnode->value(), allocator);  // then addmember("#text" , jsvalue, allocator)
    }
    else if(xmlnode->type() == rapidxml::node_element)
    {
        if(xmlnode->first_attribute())
        {
            if(xmlnode->first_node() && xmlnode->first_node()->type() == rapidxml::node_data && count_children(xmlnode) == 1)
            {
                // case: <e attr="xxx">text</e>
                rapidjson::Value jn, jv;
                jn.SetString(xmltojson_text_additional_name, allocator);
                jv.SetString(xmlnode->first_node()->value(), allocator);
                jsvalue.AddMember(jn, jv, allocator);
                xmltojson_add_attributes(xmlnode, jsvalue, allocator);
                return;
            }
            else
            {
                // case: <e attr="xxx">...</e>
                xmltojson_add_attributes(xmlnode, jsvalue, allocator);
            }
        }
        else
        {
            if(!xmlnode->first_node())
            {
                // case: <e />
                jsvalue.SetNull();
                return;
            }
            else if(xmlnode->first_node()->type() == rapidxml::node_data && count_children(xmlnode) == 1)
            {
                // case: <e>text</e>
                if (xmltojson_numeric_support == false)
                {
                    jsvalue.SetString(rapidjson::StringRef(xmlnode->first_node()->value()), allocator);
                }
                else
                {
                    bool hasDecimal;
                    if (xmltojson_has_digits_only(xmlnode->first_node()->value(), &hasDecimal) == false)
                    {
                        jsvalue.SetString(rapidjson::StringRef(xmlnode->first_node()->value()), allocator);
                    }
                    else
                    {
                        if (hasDecimal)
                        {
                            double value = std::strtod(xmlnode->first_node()->value(), nullptr);
                            jsvalue.SetDouble(value);
                        }
                        else
                        {
                            long int value = std::strtol(xmlnode->first_node()->value(), nullptr, 0);
                            jsvalue.SetInt(value);
                        }
                    }
                }
                return;
            }
        }
        if(xmlnode->first_node())
        {
            // case: complex else...
            std::map<std::string, int> name_count;
            for(xmlnode_chd = xmlnode->first_node(); xmlnode_chd; xmlnode_chd = xmlnode_chd->next_sibling())
            {
                xmltojson_add_ns_prefix(xmlnode_chd);
                xmltojson_strip_text(xmlnode_chd);

                std::string current_name;
                const char *name_ptr = NULL;
                rapidjson::Value jn, jv;
                if(xmlnode_chd->type() == rapidxml::node_data || xmlnode_chd->type() == rapidxml::node_cdata)
                {
                    current_name = xmltojson_text_additional_name;
                    name_count[current_name]++;
                    jv.SetString(xmltojson_text_additional_name, allocator);
                    name_ptr = jv.GetString();
                }
                else if(xmlnode_chd->type() == rapidxml::node_element)
                {
                    current_name = xmlnode_chd->name();
                    name_count[current_name]++;
                    name_ptr = xmlnode_chd->name();
                }
                xmltojson_traverse_node(xmlnode_chd, jsvalue_chd, allocator);
                if(name_count[current_name] > 1 && name_ptr)
                    xmltojson_to_array_form(name_ptr, jsvalue, jsvalue_chd, allocator);
                else
                {
                    jn.SetString(name_ptr, allocator);
                    jsvalue.AddMember(jn, jsvalue_chd, allocator);
                }
            }
        }
    }
    else
    {
        throw xmltojson_parse_error("Invalid data");
    }
}

std::string xmltojson(const char *xml_str)
{
    xmltojson_parse_error *error;

    try
    {
        //file<> fdoc("track_orig.xml"); // could serve another use case
        rapidxml::xml_document<> *xml_doc = new rapidxml::xml_document<>();
        xml_doc->parse<0> (const_cast<char *>(xml_str));

        rapidjson::Document js_doc;
        js_doc.SetObject();
        rapidjson::Document::AllocatorType& allocator = js_doc.GetAllocator();

        rapidxml::xml_node<> *xmlnode_chd;

        for(xmlnode_chd = xml_doc->first_node(); xmlnode_chd; xmlnode_chd = xmlnode_chd->next_sibling())
        {
            xmltojson_strip_text(xmlnode_chd);

            rapidjson::Value jsvalue_chd;
            jsvalue_chd.SetObject();
            //rapidjson::Value jsvalue_name(xmlnode_chd->name(), allocator);
            //js_doc.AddMember(jsvalue_name, jsvalue_chd, allocator);
            xmltojson_add_ns_prefix(xmlnode_chd);
            xmltojson_traverse_node(xmlnode_chd, jsvalue_chd, allocator);
            js_doc.AddMember(rapidjson::StringRef(xmlnode_chd->name()), jsvalue_chd, allocator);
        }

        rapidjson::StringBuffer buffer;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buffer);
        js_doc.Accept(writer);
        delete xml_doc;

        return buffer.GetString();
    }
    catch (xmltojson_parse_error& e) {
        error = &e;
    }
    catch (const rapidxml::parse_error& e)
    {
        error = new xmltojson_parse_error("Parse error", e);
    }
    catch (const std::runtime_error& e)
    {
        error = new xmltojson_parse_error("Runtime error", e);
    }
    catch (const std::exception& e)
    {
        error = new xmltojson_parse_error("Error", e);        
    }
    catch (...)
    {
        error = new xmltojson_parse_error("Unknown error");
    }

    return error->GetString();
}

#endif
