### Notes

* For divs class="requirement [*status here*]"
    * [*status here*] can be:
        * **Status_NONE**: I'm assuming this means that it's not actually a requirement and it just is there so the styling of the page stays the same since the styling is from 20+ years ago.
        * **STATUS_OK**: Means the requirement is already done.
        * **STATUS_NO**: Means the requirement is somehow not fulfilled yet. ***This is what we want***

### TODO / REMEMBER:
- [ ] Make a special requirement for requirements that only have text and no actual class options under the requirement. For instance, the GWAR requirement just says to "Check the University Catalog." This must be accounted for -- even beyond the GWAR and just implemented as a broad feature.

* "In Progress" requirements still might need more classes. If you are taking an Art class for a requirement, but you still have to take a Humanities class to fulfill the full requirement. It might show "In Progress" for the overall "main" requirement. Need to check this.
* Formatting is incredibly weird for certain classes. A label such as "Piano" will be labeled as a "subrequirement" but it will have no classes attached to the actual div. The two classes might be two separate divs completely below this. 
* For certain pre requirements, you have to check the "subreqPretext" to ensure that the requirement does not have a checkmark.
* Another option is always just letting people paste in their degree evaluation and then analyzing which general education classes they do not have done yet in a more manual way. They could just fill in major things on their own or something.


* There needs to be a "range" filter option for class numbers. For instance, on an art requirement degree evaluation, it says that to meet an elective you can take any class from ART 300 to 599...