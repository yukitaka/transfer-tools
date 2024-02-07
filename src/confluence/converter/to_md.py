import glob
from ..model.user import User
from ...utils import file

class Converter:
    def __init__(self, doc, path):
        self.md = "\n".join(self.to_md(doc, path))

    @staticmethod
    def to_md(doc, path):
        res = []
        if not "content" in doc:
            return
        for line in doc["content"]:
            if line["type"] == "paragraph":
                if "content" in line:
                    res += Converter.to_md(line, path)
                else:
                    res.append("\n")
            elif line["type"] == "hardBreak":
                res.append("\n")
            elif line["type"] == "text":
                if "text" not in line:
                    continue
                res.append(line["text"])
            elif line["type"] == "placeholder":
                res.append(line["attrs"]["text"])
            elif line["type"] == "mention":
                res.append("@" + User.get_user_by_id(line["attrs"]["id"]).name)
            elif line["type"] == "media" or line["type"] == "mediaInline":
                converted_line = None
                if "id" in line["attrs"]:
                    file_id = line["attrs"]["id"]
                    converted_line = "Deleted"
                    for f in glob.glob(f"{path}/attachments/*.json"):
                        d = store.load_json(f)
                        if d["fileId"] == file_id:
                            fid = d["id"]
                            name = d["title"]
                            converted_line = f"![{name}]({{{{ {fid} }}}})"
                            break
                elif "url" in line["attrs"]:
                    url = line["attrs"]["url"]
                    if "alt" in line["attrs"]:
                        alt = line["attrs"]["alt"]
                        converted_line = f"[{alt}]({url})"
                    elif line["attrs"]["type"] == "external":
                        converted_line = f"![{url}]({url})"
                if converted_line is not None:
                    res.append(converted_line)
                    continue
                return
            elif line["type"] == "emoji":
                res.append(line["attrs"]["text"])
            elif line["type"] == "status":
                st = line["attrs"]["text"]
                res.append(f"** {st} **")
            elif line["type"] == "taskItem" or line["type"] == "decisionItem":
                st = line["attrs"]["state"]
                res.append(f"** {st} **")
            elif line["type"] == "embedCard":
                if "url" in line["attrs"]:
                    url = line["attrs"]["url"]
                    res.append(f"[EmbedCard]({url})")
                    continue
                return
            elif line["type"] == "blockCard":
                if "url" in line["attrs"]:
                    url = line["attrs"]["url"]
                    res.append(f"[BlockCard]({url})")
                    continue
                return
            elif line["type"] == "inlineCard":
                if "url" in line["attrs"]:
                    url = line["attrs"]["url"]
                    res.append(f"[inlineCard]({{{{ {url} }}}})")
                    continue
                return
            elif line["type"] == "extension":
                if "extensionKey" in line["attrs"]:
                    if line["attrs"]["extensionKey"] == "lref-onedrive-embedded-file" or line["attrs"]["extensionKey"] == "lref-onedrive-files-list":
                        url = line["attrs"]["parameters"]["macroParams"]["url"]["value"]
                        res.append(f"[OneDrive]({url})")
                        continue
                    elif line["attrs"]["extensionKey"] == "style":
                        continue
                    elif line["attrs"]["extensionKey"] == "detailssummary":
                        continue
                    elif line["attrs"]["extensionKey"] == "include":
                        continue
                    elif line["attrs"]["extensionKey"] == "children":
                        res.append('$lsx()')
                        continue
                    elif line["attrs"]["extensionKey"] == "blog-posts":
                        continue
                    elif line["attrs"]["extensionKey"] == "pagetreesearch":
                        continue
                    elif line["attrs"]["extensionKey"] == "tasks-report-macro":
                        continue
                    elif line["attrs"]["extensionKey"] == "content-report-table":
                        continue
                    elif line["attrs"]["extensionKey"] == "recently-updated":
                        continue
                    elif line["attrs"]["extensionKey"] == "roadmap":
                        continue
                    elif line["attrs"]["extensionKey"] == "toc":
                        continue
                    elif line["attrs"]["extensionKey"] == "jira":
                        continue
                    elif line["attrs"]["extensionKey"] == "__confluenceADFMigrationUnsupportedContentInternalExtension__":
                        res.append(line["attrs"]["parameters"]["cxhtml"])
                        continue
            elif line["type"] == "inlineExtension":
                if "extensionKey" in line["attrs"]:
                    if line["attrs"]["extensionKey"] == "inline-external-image":
                        continue
                    elif line["attrs"]["extensionKey"] == "inline-media-image":
                        continue
                    elif line["attrs"]["extensionKey"] == "pagetree":
                        continue
                    elif line["attrs"]["extensionKey"] == "blog-posts":
                        continue
                    elif line["attrs"]["extensionKey"] == "livesearch":
                        continue
                    elif line["attrs"]["extensionKey"] == "__confluenceADFMigrationUnsupportedContentInternalExtension__":
                        res.append(line["attrs"]["parameters"]["cxhtml"])
                        continue
                    elif line["attrs"]["extensionKey"] == "lref-onedrive-file" or line["attrs"]["extensionKey"] == "lref-onedrive-files-list":
                        url = line["attrs"]["parameters"]["macroParams"]["url"]["value"]
                        res.append(f"[OneDrive]({url})")
                        continue
                    elif line["attrs"]["extensionKey"] == "jira":
                        continue
                    elif line["attrs"]["extensionKey"] == "create-from-template":
                        continue
            elif line["type"] == "rule" and len(line) == 1:
                continue
            elif "content" in line:
                res += Converter.to_md(line, path)
            else:
                return

        return res